# Copyright Tumeryk 2024

import os
import logging
import requests
from requests.exceptions import RequestException

class TumerykGuardrailsClient:
    """API Client for Tumeryk Guardrails"""

    def __init__(self, base_url: str = None):
        self.base_url = base_url or os.getenv("TUMERYK_BASE_URL", "https://chat.tmryk.com")
        self.token = None
        self.config_id = None
        self.guard_url = f"{self.base_url}/v1/chat/completions"
        self.session = requests.Session()
        self._auto_login()
        self._auto_set_policy()

    def _auto_login(self):
        """Automatically login if environment variables are available."""
        username = os.getenv("TUMERYK_USERNAME")
        password = os.getenv("TUMERYK_PASSWORD")
        if username and password:
            try:
                self.login(username, password)
            except RequestException as err:
                logging.error(f"Auto-login failed: {err}")

    def _auto_set_policy(self):
        """Automatically set policy if environment variable is available."""
        policy = os.getenv("TUMERYK_POLICY")
        if policy:
            try:
                self.set_policy(policy)
            except ValueError as err:
                logging.error(f"Auto-set policy failed: {err}")

    def _get_headers(self):
        """Helper method to get the headers including authorization."""
        if not self.token:
            raise ValueError("Authorization token is not set. Please login first.")
        return {"Authorization": f"Bearer {self.token}"}

    def login(self, username: str, password: str):
        """Authenticate and store access token."""
        username = username or os.getenv("TUMERYK_USERNAME")
        password = password or os.getenv("TUMERYK_PASSWORD")

        if not username or not password:
            raise ValueError("Username and password must be provided either as arguments or environment variables.")

        payload = {"grant_type": "password", "username": username, "password": password}
        response = self.session.post(f"{self.base_url}/auth/token", data=payload)
        response.raise_for_status()
        response_data = response.json()

        if "access_token" in response_data:
            self.token = response_data["access_token"]
        return response_data

    def get_policies(self) -> str:
        """Fetch available policies and return a list."""
        headers = self._get_headers()
        response = self.session.get(f"{self.base_url}/v1/rails/configs", headers=headers)
        response.raise_for_status()
        return [config['id'] for config in response.json()]

    def set_policy(self, config_id: str) -> str:
        """Set the configuration/policy to be used by the user."""
        if not self.token:
            raise ValueError("Authorization token is not set. Please login first.")

        self.config_id = config_id
        return {"config": f"Policy being used: {config_id}"}

    def tumeryk_completions(self, messages: str, stream: bool = False):
        """Send user input to the Guard service."""
        if not self.token:
            return {"error": "Authorization token not found. Please login to proceed."}
        if not self.config_id:
            return {"error": "Config ID is required. Please pick a policy."}

        headers = self._get_headers()
        payload = {"config_id": self.config_id, "messages": messages, "stream": stream}

        try:
            response = self.session.post(self.guard_url, json=payload, headers=headers)
            response.raise_for_status()
            return response.json()
        except RequestException as err:
            logging.error(f"Request failed: {err}")
            return {"error": f"Request failed: {err}"}
        except Exception as err:
            logging.error(f"An unexpected error occurred: {err}")
            return {"error": f"An unexpected error occurred: {err}"}

    def get_base_url(self):
        """Get the current base URL."""
        return self.base_url

    def set_base_url(self, base_url: str):
        """Set a new base URL."""
        self.base_url = base_url
        self.guard_url = f"{self.base_url}/v1/chat/completions"

    def set_token(self, token: str):
        """Set a new token directly"""
        self.token = token
