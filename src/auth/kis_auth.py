import requests
import time
from datetime import datetime, timedelta

class KISAuthenticator:
    def __init__(self, app_key, app_secret, is_paper_trading=True):
        self.app_key = app_key
        self.app_secret = app_secret
        self.base_url = "https://openapivts.koreainvestment.com:29443" if is_paper_trading else "https://openapi.koreainvestment.com:9443"
        self.token_data = None
        self.last_request_time = 0
        self.min_interval = 0.2  # 1초에 5건 제한 -> 건당 0.2초 간격

    def _wait_for_rate_limit(self):
        elapsed = time.time() - self.last_request_time
        if elapsed < self.min_interval:
            time.sleep(self.min_interval - elapsed)
        self.last_request_time = time.time()

    def get_access_token(self):
        if self.token_data is None or self._is_token_expired():
            self._request_new_token()
        return self.token_data['access_token']

    def _is_token_expired(self):
        if self.token_data is None:
            return True
        return datetime.now() >= self.token_data['expired_at']

    def revoke_token(self):
        if self.token_data is None:
            return

        url = f"{self.base_url}/oauth2/revokeP"
        payload = {
            "appkey": self.app_key,
            "appsecret": self.app_secret,
            "token": self.token_data['access_token']
        }
        
        self._wait_for_rate_limit()
        response = requests.post(url, json=payload)
        response.raise_for_status()
        self.token_data = None

    def get_approval_key(self):
        url = f"{self.base_url}/oauth2/Approval"
        payload = {
            "grant_type": "client_credentials",
            "appkey": self.app_key,
            "secretkey": self.app_secret
        }
        
        self._wait_for_rate_limit()
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json().get('approval_key')

    def _request_new_token(self):
        url = f"{self.base_url}/oauth2/tokenP"
        payload = {
            "grant_type": "client_credentials",
            "appkey": self.app_key,
            "appsecret": self.app_secret
        }
        
        self._wait_for_rate_limit()
        response = requests.post(url, json=payload)
        response.raise_for_status()
        
        data = response.json()
        expires_in = data.get('expires_in', 86400)
        
        self.token_data = {
            "access_token": data['access_token'],
            "expired_at": datetime.now() + timedelta(seconds=expires_in)
        }
