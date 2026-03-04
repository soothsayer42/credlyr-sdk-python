from typing import Optional, Dict, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from ..client import CredlyrClient


class OrgResource:
    """Organization - org settings and management."""

    def __init__(self, client: "CredlyrClient"):
        self._client = client

    def retrieve(self) -> Dict[str, Any]:
        """Get organization details."""
        result = self._client.get("/v1/org")
        return result.get("org", result)

    def update(self, **kwargs) -> Dict[str, Any]:
        """Update organization settings."""
        result = self._client.patch("/v1/org", kwargs)
        return result.get("org", result)

    def get_settings(self) -> Dict[str, Any]:
        """Get organization settings."""
        result = self._client.get("/v1/org/settings")
        return result.get("settings", result)

    def update_settings(self, **kwargs) -> Dict[str, Any]:
        """Update organization settings."""
        result = self._client.patch("/v1/org/settings", kwargs)
        return result.get("settings", result)
