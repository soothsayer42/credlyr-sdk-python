from typing import Optional, Dict, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from ..client import CredlyrClient


class PoliciesResource:
    """Policies - verification and issuance policies."""

    def __init__(self, client: "CredlyrClient"):
        self._client = client

    def list(self) -> Dict[str, Any]:
        """List all policies."""
        return self._client.get("/policies")

    def create(
        self,
        name: str,
        description: Optional[str] = None,
        pack_type: Optional[str] = None,
        rules: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Create a new policy."""
        data = {"name": name}
        if description:
            data["description"] = description
        if pack_type:
            data["pack_type"] = pack_type
        if rules:
            data["rules"] = rules
        result = self._client.post("/policies", data)
        return result.get("policy", result)

    def retrieve(self, policy_id: str) -> Dict[str, Any]:
        """Get a policy by ID."""
        result = self._client.get(f"/policies/{policy_id}")
        return result.get("policy", result)

    def update(self, policy_id: str, **kwargs) -> Dict[str, Any]:
        """Update a policy."""
        result = self._client.patch(f"/policies/{policy_id}", kwargs)
        return result.get("policy", result)

    def delete(self, policy_id: str) -> Dict[str, Any]:
        """Delete a policy."""
        return self._client.delete(f"/policies/{policy_id}")
