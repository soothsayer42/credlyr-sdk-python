from typing import Optional, Dict, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from ..client import CredlyrClient


class TeamResource:
    """Team - manage team members."""

    def __init__(self, client: "CredlyrClient"):
        self._client = client

    def list(self) -> Dict[str, Any]:
        """List all team members."""
        return self._client.get("/v1/team")

    def invite(
        self,
        email: str,
        role: str = "developer",
        name: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Invite a new team member."""
        data = {"email": email, "role": role}
        if name:
            data["name"] = name
        result = self._client.post("/v1/team", data)
        return result.get("member", result)

    def retrieve(self, user_id: str) -> Dict[str, Any]:
        """Get a team member by ID."""
        result = self._client.get(f"/v1/team/{user_id}")
        return result.get("member", result)

    def update(self, user_id: str, role: str) -> Dict[str, Any]:
        """Update a team member's role."""
        result = self._client.patch(f"/v1/team/{user_id}", {"role": role})
        return result.get("member", result)

    def remove(self, user_id: str) -> Dict[str, Any]:
        """Remove a team member."""
        return self._client.delete(f"/v1/team/{user_id}")
