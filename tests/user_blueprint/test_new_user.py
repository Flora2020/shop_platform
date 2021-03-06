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


@pytest.fixture()
def registered_user(client, csrf_token):
    data = {'csrf_token': csrf_token, 'display_name': 'pytest_user', 'email': 'pytest_user@example.com',
            'password': '12345678', 'confirm_password': '12345678'}
    client.post('/users/register', data=data)
    user = User.find_by_email(data['email'])
    yield user
    user.delete()


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


def test_unique_display_name(client, csrf_token, registered_user):
    data = {'csrf_token': csrf_token, 'display_name': registered_user.display_name, 'email': 'pytest_user2@example.com',
            'password': '12345678', 'confirm_password': '12345678'}
    response = client.post('/users/register', data=data)
    soup = BeautifulSoup(response.data, 'html.parser')
    alert_div = soup.find('div', class_='alert-warning')
    assert alert_div.string.strip() == '此顯示名稱已有人使用，請更換顯示名稱'


def test_login_page(client):
    response = client.get('/users/login')
    assert response.status_code == 200


def test_login(client, registered_user):
    data = {'display_name': registered_user.display_name, 'password': registered_user.password}
    response = client.post('/users/login', data=data)
    assert response.status_code == 200
