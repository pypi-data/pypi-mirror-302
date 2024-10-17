import requests
import re
import base64
from typing import Dict, List, Tuple
import os


class GithubAPI:
    def __init__(self, access_token: str = ""):
        self.access_token = access_token
        self.base_url = "https://api.github.com"
        self.headers = {
            "Accept": "application/vnd.github+json",
        }
        if access_token:
            self.headers["Authorization"] = f"token {access_token}"

    def parse_repo_url(self, url: str) -> Tuple[str, str, str, str]:
        url = url.rstrip("/")
        pattern = r"^https://github\.com/([^/]+)/([^/]+)(/tree/([^/]+)(/(.+))?)?$"
        match = re.match(pattern, url)
        if not match:
            raise ValueError("Invalid GitHub URL")
        owner, repo = match.group(1), match.group(2)
        ref = match.group(4) or "main"
        path = match.group(6) or ""
        return owner, repo, ref, path

    def fetch_repo_sha(self, owner: str, repo: str, ref: str, path: str) -> str:
        url = f"{self.base_url}/repos/{owner}/{repo}/contents/{path}"
        params = {"ref": ref} if ref else {}
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        content = response.json()

        if isinstance(content, list):
            # this is a directory so we need to get the commit SHA
            url = f"{self.base_url}/repos/{owner}/{repo}/commits/{ref}"
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()["sha"]
        else:
            return content["sha"]

    def fetch_repo_tree(self, owner: str, repo: str, sha: str) -> List[Dict]:
        url = f"{self.base_url}/repos/{owner}/{repo}/git/trees/{sha}"
        params = {"recursive": "1"}
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()["tree"]

    def fetch_file_contents(self, url: str) -> str:
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        content = response.json()
        # return response.json().get("content", "")

        if content.get("encoding") == "base64":
            return base64.b64decode(content["content"]).decode(
                "utf-8", errors="replace"
            )
        else:
            return content.get("content", "")

    def get_repo_contents(self, repo_url: str) -> List[Dict]:
        owner, repo, ref, path = self.parse_repo_url(repo_url)
        sha = self.fetch_repo_sha(owner, repo, ref, path)
        tree = self.fetch_repo_tree(owner, repo, sha)
        contents = []
        excluded_extensions = [
            ".gz",
            ".tar.gz",
            ".zip",
            ".whl",
            ".exe",
            ".bin",
            ".jar",
            ".war",
            ".rar",
            ".7z",
        ]
        for item in tree:
            if item["type"] == "blob":
                file_extension = os.path.splitext(item["path"])[1].lower()
                if file_extension not in excluded_extensions:
                    content = self.fetch_file_contents(item["url"])
                    contents.append(
                        {
                            "path": item["path"],
                            "content": content,
                        }
                    )
        return contents
