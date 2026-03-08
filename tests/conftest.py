"""test config"""

import pytest
from starlette.testclient import TestClient

from simon_aksw_org.app import app


@pytest.fixture(name="client")
def setup_test_client() -> TestClient:
    """Test client fixture"""
    return TestClient(app)
