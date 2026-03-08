"""Test basics"""

from http import HTTPStatus

from starlette.testclient import TestClient

from simon_aksw_org.app import app


def test_root(client: TestClient) -> None:
    """Test root page"""
    response = client.get(app.url_path_for("homepage"))
    assert response.status_code == HTTPStatus.OK


def test_favicon(client: TestClient) -> None:
    """Test favicon page"""
    response = client.get(app.url_path_for("favicon"))
    assert response.status_code == HTTPStatus.OK
