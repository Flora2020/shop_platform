import pytest
from bs4 import BeautifulSoup
from app import create_app
from models import User


@pytest.fixture()
def client():
    app = create_app()
    with app.test_client() as client:
        yield client


@pytest.fixture()
def csrf_token(client):
    response = client.get('/users/register')
    soup = BeautifulSoup(response.data, 'html.parser')
    csrf_input = soup.find(id='csrf_token')
    csrf_token = csrf_input.get('value')
    yield csrf_token


def test_get_new_user_page(client):
    response = client.get('/users/register')
    assert response.status_code == 200


def test_register_a_user(client, csrf_token):
    data = {'csrf_token': csrf_token, 'display_name': 'pytest_user', 'email': 'pytest_user@example.com',
            'password': '12345678', 'confirm_password': '12345678'}
    client.post('/users/register', data=data)

    user = User.find_by_email(data['email'])
    assert user.display_name == data['display_name'] \
           and user.email == data['email'] \
           and user.password != data['password']

    user.delete()
