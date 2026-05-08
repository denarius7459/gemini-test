import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
import time
from src.auth.kis_auth import KISAuthenticator

def test_should_enforce_rate_limit():
    # Given
    auth = KISAuthenticator("key", "secret")
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"access_token": "token", "expires_in": 3600}

    # When
    start_time = time.time()
    with patch('requests.post', return_value=mock_response):
        auth._request_new_token()
        auth._request_new_token()
    end_time = time.time()

    # Then
    # 2번 호출했으므로 최소 0.2초의 대기가 발생해야 함 (첫 호출 후 대기)
    assert end_time - start_time >= 0.2

def test_should_issue_new_token_when_no_token_exists():
    # Given
    app_key = "test_app_key"
    app_secret = "test_app_secret"
    mock_token = "mock_access_token_123"
    
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "access_token": mock_token,
        "token_type": "Bearer",
        "expires_in": 86400
    }

    # When
    with patch('requests.post', return_value=mock_response) as mock_post:
        auth = KISAuthenticator(app_key, app_secret, is_paper_trading=True)
        token = auth.get_access_token()

    # Then
    assert token == mock_token
    assert mock_post.call_count == 1

def test_should_reuse_token_when_valid_token_exists():
    # Given
    auth = KISAuthenticator("key", "secret")
    # 인위적으로 유효한 토큰 설정 (만료시간 1시간 후)
    auth.token_data = {
        "access_token": "existing_valid_token",
        "expired_at": datetime.now() + timedelta(hours=1)
    }

    # When
    with patch('requests.post') as mock_post:
        token = auth.get_access_token()

    # Then
    assert token == "existing_valid_token"
    mock_post.assert_not_called()

def test_should_revoke_token_successfully():
    # Given
    auth = KISAuthenticator("key", "secret")
    auth.token_data = {
        "access_token": "token_to_revoke",
        "expired_at": datetime.now() + timedelta(hours=1)
    }
    
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"code": 200, "message": "성공"}

    # When
    with patch('requests.post', return_value=mock_response) as mock_post:
        auth.revoke_token()

    # Then
    assert auth.token_data is None
    # /oauth2/revokeP 호출 확인
    args, kwargs = mock_post.call_args
    assert "/oauth2/revokeP" in args[0]
    assert kwargs['json']['token'] == "token_to_revoke"

def test_should_issue_approval_key():
    # Given
    auth = KISAuthenticator("key", "secret")
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"approval_key": "mock_approval_key_xyz"}

    # When
    with patch('requests.post', return_value=mock_response) as mock_post:
        approval_key = auth.get_approval_key()

    # Then
    assert approval_key == "mock_approval_key_xyz"
    # /oauth2/Approval 호출 확인
    args, kwargs = mock_post.call_args
    assert "/oauth2/Approval" in args[0]
    assert kwargs['json']['secretkey'] == "secret"
