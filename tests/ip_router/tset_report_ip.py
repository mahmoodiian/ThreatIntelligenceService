from routers.user_auth import get_new_token
from tests.test_main import client


def test_valid_ip():
    ip = '10.20.30.40'
    token = get_new_token('admin')
    response = client.post("/report-ip/", json={"ip_address": ip}, headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200
    assert "id" in response.json()


def test_invalid_ip():
    ip = '10.20.30.256'
    token = get_new_token('admin')
    response = client.post("/report-ip/", json={"ip_address": ip}, headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 422
    assert "detail" in response.json()
