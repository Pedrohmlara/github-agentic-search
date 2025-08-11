import requests
from typing import Dict, Any, List, Optional
import base64

class GitHubClient:
    GITHUB_API = "https://api.github.com"

    def __init__(self, token: str):
        if not token:
            raise RuntimeError("Missing GITHUB_TOKEN")
        self.s = requests.Session()
        self.s.headers.update({
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "agentic-search"
        })

    def _get(self, url: str, params: Dict | None = None) -> Dict:
        """
        Thin GET wrapper with JSON decoding and HTTP error raising.
        """
        r = self.s.get(url, params=params or {}, timeout=30)
        r.raise_for_status()  # raise for 4xx/5xx
        return r.json()

    def get_default_branch(self, repo: str) -> str:
        """
        Fetch repository metadata and return its default branch.
        - repo: 'owner/name'
        """
        return self._get(f"{self.GITHUB_API}/repos/{repo}").get("default_branch", "main") or "main"

    def get_tree(self, repo: str, ref: Optional[str] = None) -> List[Dict]:
        """
        Return the flattened file tree at a given ref (branch/SHA).
        """
        ref = ref or self.get_default_branch(repo)
        res = self._get(f"{self.GITHUB_API}/repos/{repo}/git/trees/{ref}", params={"recursive": "1"})
        
        return [
            {
                "type": file.get("type"),
                "path": file.get("path")
            }
            for file in res.get("tree", [])
        ]

    def get_readme(self, repo: str) -> Optional[Dict]:
        """
        Fetch README logical resource.
        """
        try:
            readme = self._get(f"{self.GITHUB_API}/repos/{repo}/readme")
        except Exception:
            return None
        
        file = self._get(f"{self.GITHUB_API}/repos/{repo}/contents/{readme['path']}")
        return {
            "path": readme["path"], 
            "content": self._decode(file)
        }

    def get_file(self, repo: str, path: str, ref: Optional[str] = None) -> Dict:
        """
        Retrieve a single file's content via contents API and base64-decode it.
        """
        params = {"ref": ref} if ref else {}
        file = self._get(f"{self.GITHUB_API}/repos/{repo}/contents/{path}", params=params)
        
        return {
            "path": path, 
            "content": self._decode(file)
        }

    def search_code(self, repo: str, query: str, per_page: int = 20) -> List[Dict]:
        """
        Perform GitHub code search scoped to a single repo.
        - repo: 'owner/name'
        - query: search expression (e.g., 'Router OR route')
        - per_page: max items to return (API limit applies)
        Returns a slim list of items with name, path, html_url, score.
        """
        q = f"{query} repo:{repo} in:file"
        data = self._get(f"{self.GITHUB_API}/search/code", params={"q": q, "per_page": per_page})
        return [
            {
                "name": it.get("name"), 
                "path": it.get("path"),
                "html_url": it.get("html_url"), 
                "score": it.get("score")
            }
            for it in data.get("items", [])
        ]

    def get_prs(self, repo: str, state: str = "all", per_page: int = 25) -> List[Dict]:
        """
        List pull requests for a repo (open/closed/all).
        """
        prs = self._get(f"{self.GITHUB_API}/repos/{repo}/pulls", params={"state": state, "per_page": per_page})
        return [
            {
                "number": pr.get("number"), 
                "title": pr.get("title"),
                "user": pr.get("user", {}).get("login"),
                "merged": pr.get("merged_at") is not None, 
                "state": pr.get("state"),
                "created_at": pr.get("created_at"), 
                "merged_at": pr.get("merged_at"),
                "html_url": pr.get("html_url")
            }
            for pr in prs
        ]

    def get_issues(self, repo: str, state: str = "all", per_page: int = 25) -> List[Dict]:
        """
        List issues (and PRs that appear in the issues feed).
        We return a compact structure noting if an item is a PR.
        """
        issues = self._get(f"{self.GITHUB_API}/repos/{repo}/issues", params={"state": state, "per_page": per_page})
        return [
            {
                "number": it.get("number"), 
                "title": it.get("title"),
                "user": it.get("user", {}).get("login"),
                "state": it.get("state"), 
                "created_at": it.get("created_at"),
                "html_url": it.get("html_url"), 
                "is_pr": "pull_request" in it
            }
            for it in issues
        ]

    @staticmethod
    def _decode(obj: Dict) -> str:
        """
        Decode a 'contents' API file payload.
        """
        c, enc = obj.get("content", ""), obj.get("encoding", "")
        if enc == "base64":
            try:
                return base64.b64decode(c).decode("utf-8", errors="ignore")
            except Exception:
                return ""
        return c