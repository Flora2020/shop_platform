import pytest
from app import create_app


@pytest.fixture()
def client():
    app = create_app()
    with app.test_client() as client:
        yield client


def test_get_new_user_page(client):
    response = client.get('/users/register')
    assert response.status_code == 200
