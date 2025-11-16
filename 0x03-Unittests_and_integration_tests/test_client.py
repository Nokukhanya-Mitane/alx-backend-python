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

from unittest.mock import patch
from parameterized import parameterized_class
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos


@parameterized_class([
    {
        "org_payload": org_payload,
        "repos_payload": repos_payload,
        "expected_repos": expected_repos,
        "apache2_repos": apache2_repos,
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """ Integration tests for GithubOrgClient.public_repos """

    @classmethod
    def setUpClass(cls):
        """ Start patching requests.get with fixture-based mock """

        def mocked_requests_get(url):
            class MockResponse:
                def __init__(self, json_data):
                    self._json_data = json_data

                def json(self):
                    return self._json_data

            if url.endswith("/orgs/testorg"):
                return MockResponse(cls.org_payload)
            if url.endswith("/orgs/testorg/repos"):
                return MockResponse(cls.repos_payload)

            return MockResponse(None)

        cls.get_patcher = patch("requests.get", side_effect=mocked_requests_get)
        cls.get_patcher.start()

    @classmethod
    def tearDownClass(cls):
        """ Stop the requests.get patcher """
        cls.get_patcher.stop()

    def test_public_repos(self):
        """ Test that public_repos returns expected repo names """
        client = GithubOrgClient("testorg")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """ Test filtering repos using Apache 2.0 license """
        client = GithubOrgClient("testorg")
        self.assertEqual(
            client.public_repos(license="apache-2.0"),
            self.apache2_repos
        )

