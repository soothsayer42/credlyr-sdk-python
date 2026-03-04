from typing import Optional, Dict, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from ..client import CredlyrClient


class BillingResource:
    """Billing - usage and subscription management."""

    def __init__(self, client: "CredlyrClient"):
        self._client = client

    def get_usage(
        self,
        meter: Optional[str] = None,
        period: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Get usage data."""
        params = {}
        if meter:
            params["meter"] = meter
        if period:
            params["period"] = period
        return self._client.get("/v1/billing/usage", params)

    def get_subscription(self) -> Dict[str, Any]:
        """Get subscription details."""
        return self._client.get("/v1/billing/subscription")

    def list_invoices(self, limit: int = 50) -> Dict[str, Any]:
        """List invoices."""
        return self._client.get("/v1/billing/invoices", {"limit": limit})

    def create_portal_session(self, return_url: Optional[str] = None) -> Dict[str, Any]:
        """Create a billing portal session."""
        data = {}
        if return_url:
            data["return_url"] = return_url
        return self._client.post("/v1/billing/portal", data)
