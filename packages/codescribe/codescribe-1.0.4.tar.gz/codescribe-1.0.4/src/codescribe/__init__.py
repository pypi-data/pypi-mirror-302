from .github_api import GithubAPI
from .formatter import format_repo_contents


def codescribe(repo_url: str, access_token: str = "") -> str:
    github_api = GithubAPI(access_token)
    contents = github_api.get_repo_contents(repo_url)
    return format_repo_contents(contents)
