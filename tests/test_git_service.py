import unittest
from unittest.mock import patch

from code_sentinel.core.git_service import git_service


class GitServiceTests(unittest.TestCase):
    @patch("code_sentinel.core.git_service.requests.get")
    def test_get_pr_diff_uses_authenticated_api(self, get):
        get.return_value.text = "diff --git a/example.py b/example.py"

        result = git_service.get_pr_diff("owner/private-repo", 7)

        self.assertEqual(result, get.return_value.text)
        get.return_value.raise_for_status.assert_called_once_with()
        args, kwargs = get.call_args
        self.assertEqual(
            args[0], "https://api.github.com/repos/owner/private-repo/pulls/7"
        )
        self.assertEqual(kwargs["headers"]["Accept"], "application/vnd.github.diff")
        self.assertTrue(kwargs["headers"]["Authorization"].startswith("Bearer "))


if __name__ == "__main__":
    unittest.main()
