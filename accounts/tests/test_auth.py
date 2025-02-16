import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken

@pytest.fixture
def create_user(db):
    """테스트용 사용자 생성"""
    user = User.objects.create_user(username="testuser", password="testpassword")
    return user

@pytest.fixture
def api_client():
    """Django REST Framework API 클라이언트"""
    return APIClient()

@pytest.fixture
def get_tokens(api_client, create_user):
    """JWT Access / Refresh Token 발급"""
    response = api_client.post("/api/token/", data={
        "username": "testuser",
        "password": "testpassword"
    })
    return response.data  # {"access": "...", "refresh": "..."}

def test_login_and_get_tokens(api_client, create_user):
    """[✔] 로그인 시 Access & Refresh Token 정상 발급 확인"""
    response = api_client.post("/api/token/", data={
        "username": "testuser",
        "password": "testpassword"
    })

    assert response.status_code == status.HTTP_200_OK
    assert "access" in response.data
    assert "refresh" in response.data
    print("\n[✅] Access & Refresh Token 발급 테스트 성공")

def test_access_protected_api(api_client, get_tokens):
    """[✔] Access Token을 이용한 보호된 API 접근 확인"""
    access_token = get_tokens["access"]
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

    response = api_client.get("/api/protected/")  

    assert response.status_code == status.HTTP_200_OK
    print("\n[✅] Access Token 보호 API 접근 테스트 성공")

def test_refresh_token(api_client, get_tokens):
    """[✔] Refresh Token을 사용하여 새로운 Access Token 발급 테스트"""
    refresh_token = get_tokens["refresh"]
    
    response = api_client.post("/api/token/refresh/", data={"refresh": refresh_token})

    assert response.status_code == status.HTTP_200_OK
    assert "access" in response.data
    print("\n[✅] Refresh Token을 통한 Access Token 갱신 성공")

def test_invalid_refresh_token(api_client):
    """[✔] 잘못된 Refresh Token 사용 시 오류 발생 확인"""
    invalid_refresh_token = "invalidtoken"

    response = api_client.post("/api/token/refresh/", data={"refresh": invalid_refresh_token})

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    print("\n[✅] 잘못된 Refresh Token 처리 테스트 성공")

@pytest.fixture
def logout_and_blacklist_token(api_client, get_tokens):
    """로그아웃 요청을 보내고 Refresh Token을 블랙리스트에 추가"""
    refresh_token = get_tokens["refresh"]
    response = api_client.post("/api/logout/", data={"refresh": refresh_token})
    return refresh_token, response

def test_logout_and_blacklist(api_client, logout_and_blacklist_token):
    """[✔] 로그아웃 시 Refresh Token 블랙리스트 추가 확인"""
    refresh_token, response = logout_and_blacklist_token

    assert response.status_code == status.HTTP_205_RESET_CONTENT
    assert BlacklistedToken.objects.filter(token=refresh_token).exists()
    print("\n[✅] 로그아웃 후 Refresh Token 블랙리스트 추가 성공")

def test_blacklisted_refresh_token(api_client, logout_and_blacklist_token):
    """[✔] 블랙리스트된 Refresh Token을 사용한 Access Token 갱신 차단"""
    refresh_token, _ = logout_and_blacklist_token

    response = api_client.post("/api/token/refresh/", data={"refresh": refresh_token})

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    print("\n[✅] 블랙리스트된 Refresh Token 차단 테스트 성공")
