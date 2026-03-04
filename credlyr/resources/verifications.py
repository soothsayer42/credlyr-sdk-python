from typing import Optional, Dict, Any, List, TYPE_CHECKING

if TYPE_CHECKING:
    from ..client import CredlyrClient


class VerificationsResource:
    """Verification sessions - verify credentials from holders."""

    def __init__(self, client: "CredlyrClient"):
        self._client = client

    def create(
        self,
        policy_id: Optional[str] = None,
        requested_claims: Optional[List[str]] = None,
        return_url: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Create a new verification session.

        Args:
            policy_id: The policy to use for verification
            requested_claims: List of claims to request
            return_url: URL to redirect after verification
            metadata: Optional metadata to attach

        Returns:
            The created verification object
        """
        data = {}
        if policy_id:
            data["policy_id"] = policy_id
        if requested_claims:
            data["requested_claims"] = requested_claims
        if return_url:
            data["return_url"] = return_url
        if metadata:
            data["metadata"] = metadata

        result = self._client.post("/v1/verifications", data)
        return result.get("verification", result)

    def retrieve(self, verification_id: str) -> Dict[str, Any]:
        """Get a verification by ID."""
        result = self._client.get(f"/v1/verifications/{verification_id}")
        return result.get("verification", result)

    def list(
        self,
        status: Optional[str] = None,
        limit: int = 50,
    ) -> Dict[str, Any]:
        """List verifications."""
        params = {"limit": limit}
        if status:
            params["status"] = status
        result = self._client.get("/v1/verifications", params)
        return result

    def get_result(self, verification_id: str) -> Dict[str, Any]:
        """Get verification result with claims."""
        result = self._client.get(f"/v1/verifications/{verification_id}/result")
        return result
