# unit tests for the codescribe package
import unittest
from unittest.mock import patch, MagicMock
from src.codescribe import codescribe, GithubAPI, format_repo_contents


# class TestCodescribe(unittest.TestCase):
#     @patch("codescribe.GithubAPI")
#     def test_codescribe(self, mock_github_api):
#         # mock the GithubAPI instance and its methods
#         mock_api_instance = mock_github_api.return_value
#         mock_api_instance.get_repo_contents.return_value = [
#             {"path": "file1.py", "content": "print('hello')"},
#             {"path": "file2.py", "content": "print('world')"},
#         ]

#         # test the codescribe function
#         result = codescribe("https://github.com/user/repo", "access_token")

#         # assert that the GitHub API was instantiated with the correct access token
#         mock_github_api.assert_called_once_with("access_token")

#         # assert that get_repo_contents was called with the correct URL
#         mock_api_instance.get_repo_contents.assert_called_once_with(
#             "https://github.com/user/repo"
#         )

#         # assert that the result contains the expected formatted content
#         self.assertIn("Directory Structure:", result)
#         self.assertIn("File: file1.py", result)
#         self.assertIn("File: file2.py", result)
#         self.assertIn("print('hello')", result)
#         self.assertIn("print('world')", result)


class TestGithubAPI(unittest.TestCase):
    def test_parse_repo_url(self):
        api = GithubAPI()

        # test valid URL
        owner, repo, ref, path = api.parse_repo_url(
            "https://github.com/user/repo/tree/main/src"
        )
        self.assertEqual(owner, "user")
        self.assertEqual(repo, "repo")
        self.assertEqual(ref, "main")
        self.assertEqual(path, "src")

        # test URL without tree
        owner, repo, ref, path = api.parse_repo_url("https://github.com/user/repo")
        self.assertEqual(owner, "user")
        self.assertEqual(repo, "repo")
        self.assertEqual(ref, "main")  # by default the branch is 'main'
        self.assertEqual(path, "")  # by defuult the path is '' (empty string)

        # test invalid URL
        with self.assertRaises(ValueError):
            api.parse_repo_url("https://invalid-url.com")

    @patch("requests.get")
    def test_fetch_repo_sha(self, mock_get):
        api = GithubAPI("access_token")
        mock_response = MagicMock()
        mock_response.json.return_value = {"sha": "abc123"}
        mock_get.return_value = mock_response

        sha = api.fetch_repo_sha("user", "repo", "main", "")

        self.assertEqual(sha, "abc123")
        mock_get.assert_called_once_with(
            "https://api.github.com/repos/user/repo/contents/",
            headers={
                "Accept": "application/vnd.github+json",
                "Authorization": "token access_token",
            },
            params={"ref": "main"},
        )

    @patch("requests.get")
    def test_fetch_repo_tree(self, mock_get):
        api = GithubAPI("access_token")
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "tree": [
                {"path": "file1.py"},
                {"path": "file2.py"},
            ]
        }
        mock_get.return_value = mock_response

        tree = api.fetch_repo_tree("user", "repo", "abc123")

        self.assertEqual(len(tree), 2)
        self.assertEqual(tree[0]["path"], "file1.py")
        self.assertEqual(tree[1]["path"], "file2.py")
        mock_get.assert_called_once_with(
            "https://api.github.com/repos/user/repo/git/trees/abc123",
            headers={
                "Accept": "application/vnd.github+json",
                "Authorization": "token access_token",
            },
            params={"recursive": "1"},
        )

    @patch("requests.get")
    def test_fetch_file_contents(self, mock_get):
        api = GithubAPI("access_token")
        mock_response = MagicMock()
        mock_response.json.return_value = {"content": "file content"}
        mock_get.return_value = mock_response

        content = api.fetch_file_contents(
            "https://api.github.com/repos/user/repo/contents/file.py"
        )

        self.assertEqual(content, "file content")
        mock_get.assert_called_once_with(
            "https://api.github.com/repos/user/repo/contents/file.py",
            headers={
                "Accept": "application/vnd.github+json",
                "Authorization": "token access_token",
            },
        )

    @patch("requests.get")
    def test_get_repo_contents(self, mock_get):
        api = GithubAPI("access_token")

        # mock the responses for fetch_repo_sha, fetch_repo_tree, and file_contents
        mock_get.side_effect = [  # control the return value for each call
            MagicMock(json=lambda: {"sha": "abc123"}),
            MagicMock(
                json=lambda: {
                    "tree": [
                        {
                            "path": "file1.py",
                            "url": "https://api.github.com/repos/user/repo/contents/file1.py",
                            "type": "blob",
                        },
                        {
                            "path": "file2.py",
                            "url": "https://api.github.com/repos/user/repo/contents/file2.py",
                            "type": "blob",
                        },
                    ]
                }
            ),
            MagicMock(json=lambda: {"content": "content1"}),
            MagicMock(json=lambda: {"content": "content2"}),
        ]

        contents = api.get_repo_contents("https://github.com/user/repo")

        self.assertEqual(len(contents), 2)
        self.assertEqual(contents[0]["path"], "file1.py")
        self.assertEqual(contents[0]["content"], "content1")
        self.assertEqual(contents[1]["path"], "file2.py")
        self.assertEqual(contents[1]["content"], "content2")


class TestFormatter(unittest.TestCase):
    def test_format_repo_contents(self):
        contents = [
            {"path": "file1.py", "content": "print('hello')"},
            {"path": "dir/file2.py", "content": "print('world')"},
        ]

        formatted = format_repo_contents(contents)

        self.assertIn("Directory Structure:", formatted)
        self.assertIn("├── file1.py", formatted)
        self.assertIn("└── dir", formatted)
        self.assertIn("    └── file2.py", formatted)
        self.assertIn("File: file1.py", formatted)
        self.assertIn("File: dir/file2.py", formatted)
        self.assertIn("print('hello')", formatted)
        self.assertIn("print('world')", formatted)


if __name__ == "__main__":
    unittest.main()
