from typing import Optional, Dict, Any, List, TYPE_CHECKING

if TYPE_CHECKING:
    from ..client import CredlyrClient


class WebhooksResource:
    """Webhooks - receive event notifications."""

    def __init__(self, client: "CredlyrClient"):
        self._client = client

    def list(self, project_id: Optional[str] = None) -> Dict[str, Any]:
        """List all webhooks."""
        params = {}
        if project_id:
            params["project_id"] = project_id
        return self._client.get("/webhooks", params)

    def create(
        self,
        url: str,
        events: List[str],
        project_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Create a new webhook."""
        data = {"url": url, "events": events}
        if project_id:
            data["project_id"] = project_id
        result = self._client.post("/webhooks", data)
        return result.get("webhook", result)

    def update(
        self,
        webhook_id: str,
        url: Optional[str] = None,
        events: Optional[List[str]] = None,
        enabled: Optional[bool] = None,
    ) -> Dict[str, Any]:
        """Update a webhook."""
        data = {}
        if url is not None:
            data["url"] = url
        if events is not None:
            data["events"] = events
        if enabled is not None:
            data["enabled"] = enabled
        result = self._client.patch(f"/webhooks/{webhook_id}", data)
        return result.get("webhook", result)

    def delete(self, webhook_id: str) -> Dict[str, Any]:
        """Delete a webhook."""
        return self._client.delete(f"/webhooks/{webhook_id}")

    def rotate_secret(self, webhook_id: str) -> Dict[str, Any]:
        """Rotate webhook signing secret."""
        return self._client.post(f"/webhooks/{webhook_id}/rotate")
