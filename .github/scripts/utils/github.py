from typing import Dict, List

import requests
from config import GithubConfig
from result import Err, Ok, Result
from yarl import URL


class GitHubAPIUtils:
    _base_url = URL("https://api.github.com")

    @classmethod
    def _get_base_repo_url(cls, owner: str, repo: str) -> URL:
        return cls._base_url / "repos" / owner / repo

    @classmethod
    def create_issue(
        cls,
        title: str = "No Title Given",
        body: str = "No Body Given",
        assignees: List[str] = [],
        labels: List[str] = [],
        milestone: str = None,
        repo_owner: str = GithubConfig.REPO_OWNER,
        repo_name: str = GithubConfig.REPO_NAME,
        token: str = GithubConfig.TOKEN,
    ) -> Result[None, str]:
        url = cls._get_base_repo_url(repo_owner, repo_name) / "issues"
        headers = {
            "Accept": "application/vnd.github.v3+json",
            "Authorization": f"token {token}",
        }
        data = {
            "title": title,
            "body": body,
            "assignees": assignees,
            "labels": labels,
            "milestone": milestone,
        }

        response = requests.post(url.__str__(), headers=headers, json=data)

        if response.status_code == 201:
            return Ok(None)

        return Err(response.json())

    @classmethod
    def get_open_issues(
        cls,
        repo_owner: str = GithubConfig.REPO_OWNER,
        repo_name: str = GithubConfig.REPO_NAME,
        token: str = GithubConfig.TOKEN,
    ) -> Result[Dict, Dict]:
        url = cls._get_base_repo_url(repo_owner, repo_name) / "issues"
        headers = {
            "Accept": "application/vnd.github.v3+json",
            "Authorization": f"token {token}",
        }
        params = {"state": "open"}

        response = requests.get(url.__str__(), headers=headers, params=params)

        json = response.json()

        if response.status_code == 200:
            return Ok(json)

        return Err(json)
