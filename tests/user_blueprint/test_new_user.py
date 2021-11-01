import requests

URL = 'http://127.0.0.1:5000/users/register'


def test_get_new_user_page():
    req = requests.request('GET', URL)
    assert req.status_code == 200
