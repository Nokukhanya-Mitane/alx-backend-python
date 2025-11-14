#!/usr/bin/env python3
"""Unit tests for utils.access_nested_map"""

from unittest.mock import patch
from parameterized import parameterized
from utils import get_json
import unittest

class TestGetJson(unittest.TestCase):
    """Tests for utils.get_json"""

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"status": "ok"}),
    ])
    @patch("utils.requests.get")
    def test_get_json(self, test_url, expected_payload, mock_get):
        """Test that get_json returns the correct JSON response."""
        mock_get.return_value.json.return_value = expected_payload

        result = get_json(test_url)

        mock_get.assert_called_once_with(test_url)
        self.assertEqual(result, expected_payload)
