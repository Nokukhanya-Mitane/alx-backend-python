#!/usr/bin/env python3
"""
Unit tests for GithubOrgClient
"""

import unittest
from unittest.mock import patch
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """
    Test case class for GithubOrgClient.org method
    """

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """
        Test that GithubOrgClient.org returns correct JSON response
        and calls get_json once with expected URL
        """
        expected_value = {"payload": org_name}
        mock_get_json.return_value = expected_value

        client = GithubOrgClient(org_name)
        result = client.org

        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )
        self.assertEqual(result, expected_value)


if __name__ == '__main__':
    unittest.main()
    def test_public_repos_url(self):
        """Test the _public_repos_url property"""

        payload = {"repos_url": "https://api.github.com/orgs/test/repos"}

        with patch("client.GithubOrgClient.org", new_callable=property) as mock_org:
            mock_org.return_value = payload
            client = GithubOrgClient("test")
            result = client._public_repos_url

            self.assertEqual(result, payload["repos_url"])
