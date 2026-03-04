from typing import Optional, Dict, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from ..client import CredlyrClient


class ProjectsResource:
    """Projects - separate environments within your org."""

    def __init__(self, client: "CredlyrClient"):
        self._client = client

    def list(self) -> Dict[str, Any]:
        """List all projects."""
        return self._client.get("/projects")

    def create(self, name: str, environment: str = "sandbox") -> Dict[str, Any]:
        """Create a new project."""
        result = self._client.post("/projects", {"name": name, "environment": environment})
        return result.get("project", result)

    def retrieve(self, project_id: str) -> Dict[str, Any]:
        """Get a project by ID."""
        result = self._client.get(f"/projects/{project_id}")
        return result.get("project", result)

    def delete(self, project_id: str) -> Dict[str, Any]:
        """Delete a project."""
        return self._client.delete(f"/projects/{project_id}")
