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

class TestMemoize(unittest.TestCase):
    """Tests for the memoize decorator"""

    def test_memoize(self):
        """Test that a_method is only called once due to memoization"""

        class TestClass:
            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        with patch.object(TestClass, "a_method", return_value=42) as mock_method:
            obj = TestClass()

            # First call - method runs
            self.assertEqual(obj.a_property, 42)

            # Second call - should use cached value
            self.assertEqual(obj.a_property, 42)

            mock_method.assert_called_once()
