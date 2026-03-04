from typing import Optional, Dict, Any, List, TYPE_CHECKING

if TYPE_CHECKING:
    from ..client import CredlyrClient


class IssuersResource:
    """Issuers - trusted credential issuers (trust registry)."""

    def __init__(self, client: "CredlyrClient"):
        self._client = client

    def list(self) -> Dict[str, Any]:
        """List all trusted issuers."""
        return self._client.get("/trust/issuers")

    def create(
        self,
        name: str,
        domain: Optional[str] = None,
        allowed_credential_types: Optional[List[str]] = None,
        assurance_level: str = "basic",
    ) -> Dict[str, Any]:
        """Create a new trusted issuer."""
        data = {"name": name, "assurance_level": assurance_level}
        if domain:
            data["domain"] = domain
        if allowed_credential_types:
            data["allowed_credential_types"] = allowed_credential_types
        result = self._client.post("/trust/issuers", data)
        return result.get("issuer", result)

    def retrieve(self, issuer_id: str) -> Dict[str, Any]:
        """Get an issuer by ID."""
        result = self._client.get(f"/trust/issuers/{issuer_id}")
        return result.get("issuer", result)

    def update(self, issuer_id: str, **kwargs) -> Dict[str, Any]:
        """Update an issuer."""
        result = self._client.patch(f"/trust/issuers/{issuer_id}", kwargs)
        return result.get("issuer", result)

    def delete(self, issuer_id: str) -> Dict[str, Any]:
        """Delete an issuer."""
        return self._client.delete(f"/trust/issuers/{issuer_id}")

    def list_keys(self, issuer_id: str) -> Dict[str, Any]:
        """List keys for an issuer."""
        return self._client.get(f"/trust/issuers/{issuer_id}/keys")

    def add_key(
        self,
        issuer_id: str,
        jwks_uri: Optional[str] = None,
        public_key_jwk: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Add a key to an issuer."""
        data = {}
        if jwks_uri:
            data["jwks_uri"] = jwks_uri
        if public_key_jwk:
            data["public_key_jwk"] = public_key_jwk
        result = self._client.post(f"/trust/issuers/{issuer_id}/keys", data)
        return result.get("key", result)

    def delete_key(self, issuer_id: str, key_id: str) -> Dict[str, Any]:
        """Delete a key from an issuer."""
        return self._client.delete(f"/trust/issuers/{issuer_id}/keys/{key_id}")
