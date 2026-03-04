from typing import Optional, Dict, Any, List, TYPE_CHECKING

if TYPE_CHECKING:
    from ..client import CredlyrClient


class ExportsResource:
    """Exports - evidence bundle exports."""

    def __init__(self, client: "CredlyrClient"):
        self._client = client

    def list(self, limit: int = 50) -> Dict[str, Any]:
        """List exports."""
        return self._client.get("/v1/exports", {"limit": limit})

    def create(
        self,
        verification_ids: Optional[List[str]] = None,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
        format: str = "json",
    ) -> Dict[str, Any]:
        """Create a new export."""
        data = {"format": format}
        if verification_ids:
            data["verification_ids"] = verification_ids
        if date_from:
            data["date_from"] = date_from
        if date_to:
            data["date_to"] = date_to
        result = self._client.post("/v1/exports", data)
        return result.get("export", result)

    def retrieve(self, export_id: str) -> Dict[str, Any]:
        """Get an export by ID."""
        result = self._client.get(f"/v1/exports/{export_id}")
        return result.get("export", result)

    def get_download_url(self, export_id: str) -> Dict[str, Any]:
        """Get export download URL."""
        return self._client.get(f"/v1/exports/{export_id}/download")
