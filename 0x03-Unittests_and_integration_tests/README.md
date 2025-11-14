📘 0x03-Unittests and Integration Tests

This project focuses on writing unit tests and integration tests in Python using the built-in unittest framework.
You will also use:

parameterized for parameterized test cases

mock for mocking external services

fixtures for integration testing with real data

best practices for test structure and naming

📌 Learning Objectives

By the end of this project, you should be able to:

Write unit tests using the unittest module

Parameterize tests for multiple test cases

Mock external API calls with unittest.mock

Test exceptions and edge cases

Write integration tests that use real network calls or data

Organize tests following Python best practices

🧪 Project Structure
0x03-Unittests_and_integration_tests/
│
├── test_utils.py          # Unit tests for utils module
├── test_client.py         # Unit tests for API Client (mocking)
├── test_integration.py    # Integration tests with fixtures
│
├── fixtures/              # Contains fixture JSON files
│   └── github_org.json
│
├── utils.py               # Utilities to be tested
├── client.py              # API client class
│
└── README.md              # Project documentation

📝 Task Overview
0. Parameterize a Unit Test

Write tests for utils.access_nested_map

Use parameterized.expand

Assert correct return values

1. Test KeyError Exceptions

Ensure the function raises the correct exception for invalid paths

2. Mock HTTP Calls

Mock requests.get

Test JSON responses without calling the real API

3. Test Memoization Decorator

Ensure value is computed only once

4–5. Testing Client Classes

Mock API responses

Handle endpoints, organization data, repo lists

6–7. Integration Testing

Use fixtures from fixtures/ directory

Perform real flow tests without mocking

▶️ Running Tests

To run all tests:

python3 -m unittest discover -v


Run a single test file:

python3 -m unittest test_utils.py

📚 Requirements

Python 3.7+

parameterized package
Install:

pip install parameterized
