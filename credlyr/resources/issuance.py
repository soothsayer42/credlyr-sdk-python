from typing import Optional, Dict, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from ..client import CredlyrClient


class IssuanceResource:
    """Issuance sessions - issue credentials to holders."""

    def __init__(self, client: "CredlyrClient"):
        self._client = client

    def create_session(
        self,
        credential_type: str,
        claims: Dict[str, Any],
        expires_in: Optional[int] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Create a new issuance session.

        Args:
            credential_type: Type of credential to issue
            claims: Claims to include in the credential
            expires_in: Session expiry in seconds
            metadata: Optional metadata

        Returns:
            The created issuance session
        """
        data = {
            "credential_type": credential_type,
            "claims": claims,
        }
        if expires_in:
            data["expires_in"] = expires_in
        if metadata:
            data["metadata"] = metadata

        result = self._client.post("/v1/issuance_sessions", data)
        return result.get("issuance_session", result)

    def get_session(self, session_id: str) -> Dict[str, Any]:
        """Get an issuance session by ID."""
        result = self._client.get(f"/v1/issuance_sessions/{session_id}")
        return result.get("issuance_session", result)

    def list_sessions(self, limit: int = 50) -> Dict[str, Any]:
        """List issuance sessions."""
        result = self._client.get("/v1/issuance_sessions", {"limit": limit})
        return result
