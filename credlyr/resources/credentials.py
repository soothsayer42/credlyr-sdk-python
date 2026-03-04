from typing import Optional, Dict, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from ..client import CredlyrClient


class CredentialsResource:
    """Credentials - manage issued credentials."""

    def __init__(self, client: "CredlyrClient"):
        self._client = client

    def list(
        self,
        holder_id: Optional[str] = None,
        credential_type: Optional[str] = None,
        status: Optional[str] = None,
        limit: int = 50,
    ) -> Dict[str, Any]:
        """List credentials."""
        params = {"limit": limit}
        if holder_id:
            params["holder_id"] = holder_id
        if credential_type:
            params["credential_type"] = credential_type
        if status:
            params["status"] = status
        result = self._client.get("/v1/credentials", params)
        return result

    def retrieve(self, credential_id: str) -> Dict[str, Any]:
        """Get a credential by ID."""
        result = self._client.get(f"/v1/credentials/{credential_id}")
        return result.get("credential", result)

    def revoke(self, credential_id: str, reason: Optional[str] = None) -> Dict[str, Any]:
        """Revoke a credential."""
        data = {}
        if reason:
            data["reason"] = reason
        result = self._client.post(f"/v1/credentials/{credential_id}/revoke", data)
        return result.get("credential", result)

    def get_status(self, handle: str) -> Dict[str, Any]:
        """Get credential status by handle."""
        result = self._client.get(f"/v1/status/{handle}")
        return result
