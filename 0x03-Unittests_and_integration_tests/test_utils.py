#!/usr/bin/env python3
#!/usr/bin/env python3
"""Unit tests for utils module."""

import unittest
from unittest.mock import patch
from parameterized import parameterized

from utils import access_nested_map, get_json, memoize


class TestAccessNestedMap(unittest.TestCase):
    """Tests for access_nested_map."""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """Test correct return values."""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",), "'a'"),
        ({"a": 1}, ("a", "b"), "'b'"),
    ])
    def test_access_nested_map_exception(
        self, nested_map, path, expected_message
    ):
        """Test KeyError is raised with correct message."""
        with self.assertRaises(KeyError) as err:
            access_nested_map(nested_map, path)
        self.assertEqual(str(err.exception), expected_message)


class TestGetJson(unittest.TestCase):
    """Tests for get_json."""

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"status": "ok"}),
    ])
    @patch("utils.requests.get")
    def test_get_json(self, test_url, expected_payload, mock_get):
        """Test JSON response is returned correctly."""
        mock_get.return_value.json.return_value = expected_payload

        result = get_json(test_url)

        mock_get.assert_called_once_with(test_url)
        self.assertEqual(result, expected_payload)


class TestMemoize(unittest.TestCase):
    """Tests for memoize decorator."""

    def test_memoize(self):
        """Test that a_method is only called once."""

        class TestClass:
            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        with patch.object(TestClass, "a_method", return_value=42) as mock_m:
            obj = TestClass()

            self.assertEqual(obj.a_property, 42)
            self.assertEqual(obj.a_property, 42)

            mock_m.assert_called_once()
