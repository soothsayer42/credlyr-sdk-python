from typing import Optional, Dict, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from ..client import CredlyrClient


class ApiKeysResource:
    """API Keys - manage programmatic access."""

    def __init__(self, client: "CredlyrClient"):
        self._client = client

    def list(self, project_id: Optional[str] = None) -> Dict[str, Any]:
        """List all API keys."""
        params = {}
        if project_id:
            params["project_id"] = project_id
        return self._client.get("/api_keys", params)

    def create(self, name: str, project_id: str) -> Dict[str, Any]:
        """Create a new API key."""
        result = self._client.post("/api_keys", {"name": name, "project_id": project_id})
        return result

    def revoke(self, key_id: str) -> Dict[str, Any]:
        """Revoke an API key."""
        return self._client.delete(f"/api_keys/{key_id}")
