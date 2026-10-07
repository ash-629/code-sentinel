import logging

import requests
from github import Github

from code_sentinel.config import config
from code_sentinel.core.git_provider import GitProvider

logger = logging.getLogger(__name__)

class GitService(GitProvider):

    def __init__(self):
        token = config.GITHUB_TOKEN
        if not token:
            logger.error("GITHUB_TOKEN not set")
            raise ValueError("GITHUB_TOKEN not set")
        self.client = Github(token)

    def get_pr_diff(self, repo_name: str, pr_number: int) -> str:
        """
        get diff
        :param repo_name:
        :param pr_number:
        :return:
        """
        headers = {
            "Authorization": f"Bearer {config.GITHUB_TOKEN}",
            "Accept": "application/vnd.github.diff",
            "User-Agent": "code-sentinel",
        }

        # The web diff_url may return 404 for private repositories even with an API token.
        response = requests.get(
            f"https://api.github.com/repos/{repo_name}/pulls/{pr_number}",
            headers=headers,
            timeout=30,
        )
        response.raise_for_status() # raise error if request failed

        return response.text

    def post_comment(self, repo_name: str, pr_number: int, comment: str):
        """
        post comment to pr
        :param repo_name:
        :param pr_number:
        :param comment:
        :return:
        """
        repo = self.client.get_repo(repo_name)
        pr = repo.get_pull(pr_number)

        formatted_comment = f"## Code Review Comments by Code-Sentinel:\n\n{comment}"
        pr.create_issue_comment(formatted_comment)

# singleton     instance
git_service = GitService()

