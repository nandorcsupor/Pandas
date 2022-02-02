import pytest
import requests
import json

def main_url():
    return "https://reqres.in/"


def test_valid_login(main_url):
    url = main_url + "/api/login/"
    data = ('email': 'abc.xyz.com', 'password': 'qwerty')
    response = requests.get(url, data = data)
    token = json.loads(response.text)
    assert response.status_code == 200
    assert token["token"] == "asd"