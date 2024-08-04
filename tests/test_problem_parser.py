import pytest
import requests_mock
from unittest.mock import MagicMock
from func import problem_parser, db_manager
from func.problem_parser import parsing_code


@pytest.fixture
def mock_db_manager():
    mock_db = MagicMock()
    db_manager.DBManager = MagicMock(return_value=mock_db)
    return mock_db


def test_parsing_code(mock_db_manager):
    # Mock the API response
    api_url = "https://codeforces.com/api/problemset.problems"
    api_response = {
        "result": {
            "problems": [
                {
                    "contestId": 123,
                    "index": "A",
                    "name": "Sample Problem",
                    "rating": 1500,
                    "tags": ["dp", "math"],
                }
            ],
            "problemStatistics": [
                {"contestId": 123, "index": "A", "solvedCount": 1000}
            ],
        }
    }

    with requests_mock.Mocker() as m:
        m.get(api_url, json=api_response)
        parsing_code()

    # Assertions to check if the database methods were called correctly
    mock_db_manager.db_update_problem.assert_called_with(
        123, "A", "Sample Problem", 1500, ["dp", "math"]
    )
    mock_db_manager.db_add_problem.assert_called_with(
        123,
        "A",
        "Sample Problem",
        "https://codeforces.com/problemset/problem/123/A",
        1500,
        ["dp", "math"],
    )
    mock_db_manager.db_add_tag.assert_any_call(123, "A", "dp")
    mock_db_manager.db_add_tag.assert_any_call(123, "A", "math")
    mock_db_manager.db_add_problem_solvedcount.assert_called_with(123, "A", 1000)
