import pytest
from unittest.mock import patch, MagicMock
from psycopg2 import DatabaseError

from func.db_manager import DBManager


@pytest.fixture
def mock_connection():
    with patch("psycopg2.connect") as mock_connect:
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        yield mock_conn, mock_cursor


@pytest.fixture
def db_manager(mock_connection):
    return DBManager()


def test_qw_success(db_manager, mock_connection):
    mock_conn, mock_cursor = mock_connection
    mock_cursor.fetchall.return_value = [("result",)]

    result = db_manager.qw("SELECT * FROM table")

    assert result == [("result",)]
    mock_cursor.execute.assert_called_once_with("SELECT * FROM table")


def test_qw_failure(db_manager, mock_connection):
    mock_conn, mock_cursor = mock_connection
    mock_cursor.execute.side_effect = DatabaseError("Database error")

    with pytest.raises(DatabaseError):
        db_manager.qw("SELECT * FROM table")


def test_db_add_problem(db_manager, mock_connection):
    mock_conn, mock_cursor = mock_connection

    db_manager.db_add_problem(
        123, "A", "Problem Name", "http://example.com", 1500, '["tag1", "tag2"]'
    )

    mock_cursor.execute.assert_called_once_with(
        "INSERT INTO public.problem(id_problem, name, contestId, index, url, rating, tags) "
        "select %s, %s, %s, %s, %s, %s, %s where not exists "
        "(select id_problem from problem where id_problem='123A')",
        (
            "123A",
            "Problem Name",
            123,
            "A",
            "http://example.com",
            1500,
            '["tag1", "tag2"]',
        ),
    )


def test_db_update_problem(db_manager, mock_connection):
    mock_conn, mock_cursor = mock_connection

    db_manager.db_update_problem(123, "A", "Updated Problem Name", 1600, '["tag3"]')

    mock_cursor.execute.assert_called_once_with(
        "UPDATE public.problem "
        "SET  name=%s, rating=%s, tags=%s where id_problem='123A'",
        ("Updated Problem Name", 1600, '["tag3"]'),
    )


def test_db_add_tag(db_manager, mock_connection):
    mock_conn, mock_cursor = mock_connection

    db_manager.db_add_tag(123, "A", "tag4")

    mock_cursor.execute.assert_called_once_with(
        "INSERT INTO public.problem_tags(id_problem, tag) "
        "select %s, %s where not exists (select id_problem from problem_tags where id_problem='123A' "
        "and tag='tag4')",
        ("123A", "tag4"),
    )


def test_db_add_problem_solvedcount(db_manager, mock_connection):
    mock_conn, mock_cursor = mock_connection

    db_manager.db_add_problem_solvedcount(123, "A", 100)

    mock_cursor.execute.assert_called_once_with(
        "UPDATE public.problem " "SET solvedCount = %s where id_problem='123A'", (100,)
    )
