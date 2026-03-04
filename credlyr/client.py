import httpx
from typing import Optional, Dict, Any, List
import time

from .errors import (
    CredlyrError,
    AuthenticationError,
    RateLimitError,
    NotFoundError,
    ValidationError,
    ServerError,
)
from .resources import (
    VerificationsResource,
    IssuanceResource,
    CredentialsResource,
    PoliciesResource,
    IssuersResource,
    ProjectsResource,
    ApiKeysResource,
    WebhooksResource,
    TeamResource,
    BillingResource,
    ExportsResource,
    OrgResource,
)


class CredlyrClient:
    """
    Official Credlyr API client for Python.

    Example:
        >>> client = CredlyrClient(api_key="sk_live_xxx")
        >>> verification = client.verifications.create(
        ...     policy_id="pol_123",
        ...     return_url="https://example.com/callback"
        ... )
    """

    DEFAULT_BASE_URL = "https://api.credlyr.com"
    DEFAULT_TIMEOUT = 30.0
    DEFAULT_MAX_RETRIES = 2

    def __init__(
        self,
        api_key: str,
        base_url: Optional[str] = None,
        timeout: Optional[float] = None,
        max_retries: Optional[int] = None,
    ):
        """
        Initialize the Credlyr client.

        Args:
            api_key: Your Credlyr API key
            base_url: Custom API base URL (optional)
            timeout: Request timeout in seconds (default: 30)
            max_retries: Maximum retries for failed requests (default: 2)
        """
        self.api_key = api_key
        self.base_url = (base_url or self.DEFAULT_BASE_URL).rstrip("/")
        self.timeout = timeout or self.DEFAULT_TIMEOUT
        self.max_retries = max_retries if max_retries is not None else self.DEFAULT_MAX_RETRIES

        self._client = httpx.Client(
            base_url=self.base_url,
            timeout=self.timeout,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "User-Agent": "credlyr-python/1.0.0",
            },
        )

        # Initialize resources
        self.verifications = VerificationsResource(self)
        self.issuance = IssuanceResource(self)
        self.credentials = CredentialsResource(self)
        self.policies = PoliciesResource(self)
        self.issuers = IssuersResource(self)
        self.projects = ProjectsResource(self)
        self.api_keys = ApiKeysResource(self)
        self.webhooks = WebhooksResource(self)
        self.team = TeamResource(self)
        self.billing = BillingResource(self)
        self.exports = ExportsResource(self)
        self.org = OrgResource(self)

    def _request(
        self,
        method: str,
        path: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Make an API request with retry logic."""
        last_error = None

        for attempt in range(self.max_retries + 1):
            try:
                response = self._client.request(
                    method=method,
                    url=path,
                    json=data,
                    params=params,
                )

                request_id = response.headers.get("X-Request-Id", "")

                if response.status_code == 429:
                    retry_after = int(response.headers.get("Retry-After", 60))
                    if attempt < self.max_retries:
                        time.sleep(retry_after)
                        continue
                    raise RateLimitError(retry_after, request_id)

                if response.status_code >= 500 and attempt < self.max_retries:
                    time.sleep(min(0.5 * (2 ** attempt), 30))
                    continue

                result = response.json() if response.content else {}

                if not response.is_success:
                    error = result.get("error", {})
                    code = error.get("code", "error")
                    message = error.get("message", "Unknown error")

                    if response.status_code == 400:
                        raise ValidationError(message, error.get("param"), request_id)
                    elif response.status_code == 401:
                        raise AuthenticationError(message, request_id)
                    elif response.status_code == 404:
                        raise NotFoundError("resource", path, request_id)
                    elif response.status_code >= 500:
                        raise ServerError(message, request_id)
                    else:
                        raise CredlyrError(code, message, response.status_code, request_id)

                return result

            except httpx.HTTPError as e:
                last_error = e
                if attempt < self.max_retries:
                    time.sleep(min(0.5 * (2 ** attempt), 30))
                    continue

        raise last_error or Exception("Request failed")

    def get(self, path: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make a GET request."""
        return self._request("GET", path, params=params)

    def post(self, path: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make a POST request."""
        return self._request("POST", path, data=data)

    def patch(self, path: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make a PATCH request."""
        return self._request("PATCH", path, data=data)

    def delete(self, path: str) -> Dict[str, Any]:
        """Make a DELETE request."""
        return self._request("DELETE", path)

    def close(self):
        """Close the HTTP client."""
        self._client.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
