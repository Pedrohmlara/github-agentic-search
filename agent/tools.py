import os
from agents.tool import function_tool as tool
from dotenv import load_dotenv
from typing import Dict, Any, List, Optional
from agent.client.github import GitHubClient

load_dotenv()
_gh = GitHubClient(os.getenv("GITHUB_TOKEN"))

@tool
def list_repo_tree(repo: str, ref: Optional[str] = None) -> Dict[str, Any]:
    """List repository tree; returns files and dirs."""
    tree = _gh.get_tree(repo, ref)
    return {
        "total": len(tree),
        "files": [t for t in tree if t.get("type") == "blob"][:500],
        "dirs": [t for t in tree if t.get("type") == "tree"][:500],
    }

@tool
def get_readme(repo: str) -> Dict[str, Any]:
    """Fetch README content if present."""
    rd = _gh.get_readme(repo)
    return rd or {"path": None, "content": ""}


@tool
def search_code(repo: str, query: str, per_page: int = 20) -> Dict[str, Any]:
    """Search code within the repository."""
    return {"results": _gh.search_code(repo, query, per_page)}


@tool
def get_file_content(repo: str, path: str, ref: Optional[str] = None) -> Dict[str, Any]:
    """Read a specific file content by path."""
    return _gh.get_file(repo, path, ref)


@tool
def get_prs(repo: str, state: str = "all", per_page: int = 25) -> Dict[str, Any]:
    """List recent pull requests."""
    return {"pull_requests": _gh.get_prs(repo, state, per_page)}


@tool
def get_issues(repo: str, state: str = "all", per_page: int = 25) -> Dict[str, Any]:
    """List recent issues."""
    return {"issues": _gh.get_issues(repo, state, per_page)}