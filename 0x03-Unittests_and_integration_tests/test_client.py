#!/usr/bin/env python3
"""
Unittests for client.GithubOrgClient
"""

import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized

from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """ Tests for GithubOrgClient """

    @parameterized.expand([
        ("google",),
        ("abc",)
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """ Test GithubOrgClient.org returns expected data """
        test_payload = {"payload": True}
        mock_get_json.return_value = test_payload

        client = GithubOrgClient(org_name)
        self.assertEqual(client.org, test_payload)
        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")

    @patch.object(GithubOrgClient, 'org', new_callable=PropertyMock)
    def test_public_repos_url(self, mock_org):
        """ Test _public_repos_url property """
        mock_org.return_value = {"repos_url": "http://example.com/repos"}

        client = GithubOrgClient("example")
        self.assertEqual(client._public_repos_url, "http://example.com/repos")


if __name__ == "__main__":
    unittest.main()

    unittest.main()
    def test_public_repos_url(self):
        """Test the _public_repos_url property"""

        payload = {"repos_url": "https://api.github.com/orgs/test/repos"}

        with patch("client.GithubOrgClient.org", new_callable=property) as mock_org:
            mock_org.return_value = payload
            client = GithubOrgClient("test")
            result = client._public_repos_url

            self.assertEqual(result, payload["repos_url"])
    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """Test public_repos returns expected list of repos"""
        test_repos_payload = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"}
        ]
        mock_get_json.return_value = test_repos_payload

        with patch('client.GithubOrgClient._public_repos_url',
                   new_callable=property) as mock_public_repos_url:
            mock_public_repos_url.return_value = "mocked_url"
            client = GithubOrgClient("test-org")
            result = client.public_repos()

        expected = ["repo1", "repo2", "repo3"]
        self.assertEqual(result, expected)

        mock_public_repos_url.assert_called_once()
        mock_get_json.assert_called_once_with("mocked_url")

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """ Test GithubOrgClient.has_license method """
        client = GithubOrgClient("example")
        result = client.has_license(repo, license_key)
        self.assertEqual(result, expected)
