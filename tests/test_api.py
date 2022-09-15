import pytest


@pytest.fixture()
def format_res(client):
    conf = """
        [sqlfluff:rules:L010]
        capitalisation_policy = lower
        """
    request = {"dialect": "ansi", "conf": conf, "sql": "SELECT 1 FROM AWESOME_table\n"}
    return client.post("/v1/pretty", json=request)


def test_get_root(client):
    response = client.get("/")
    assert response.text == "Welcome to sqlfluff-api!"


def test_format_status(format_res):
    assert format_res.status_code == 200


def test_format_sql(format_res):
    assert format_res.get_json()["sql"] == "select 1 from AWESOME_TABLE\n"


def test_format_lint(format_res):
    assert format_res.get_json()["lint"] == [
        {
            "code": "L010",
            "description": "Keywords must be lower case.",
            "line_no": 1,
            "line_pos": 1,
        },
        {
            "code": "L010",
            "description": "Keywords must be lower case.",
            "line_no": 1,
            "line_pos": 10,
        },
        {
            "code": "L014",
            "description": "Unquoted identifiers must " "be consistently upper case.",
            "line_no": 1,
            "line_pos": 15,
        },
    ]
