# Copyright Tumeryk 2024

import os
import requests
from requests.exceptions import RequestException

class TumerykGuardrailsClient:
    """API Client for Tumeryk Guardrails"""

    def __init__(self, base_url="https://chat.tmryk.com"):
        self.base_url = base_url 
        self.token = None
        self.config_id =  None
        self.headers = None
        self.guard_url = f"{self.base_url}/v1/chat/completions"
    
    def _get_headers(self):
        """Helper method to get the headers including authorization."""
        if not self.token:
            raise ValueError("Authorization token is not set. Please login first.")
        if not self.headers:
            self.headers = {"Authorization": f"Bearer {self.token}"}
        return self.headers

    def login(self, username: str, password: str):
        """Authenticate and store access token."""
        payload = {"grant_type": "password", "username": username, "password": password}
        response = requests.post(f"{self.base_url}/auth/token", data=payload)
        response.raise_for_status()
        response_data = response.json()

        if "access_token" in response_data:
            self.token = response_data["access_token"]
            self.headers = None
        return response_data

    def get_policies(self):
        """Fetch available policies and return a list."""
        headers = self._get_headers()
        response = requests.get(f"{self.base_url}/v1/rails/configs", headers=headers)
        response.raise_for_status()
        return [config['id'] for config in response.json()]
    
    def set_policy(self, config_id: str):
        """Set the configuration/policy to be used by the user."""
        if not self.token:
            raise ValueError("Authorization token is not set. Please login first.")

        self.config_id = config_id
        return {"config": f"Policy being used: {config_id}"}

    def tumeryk_completions(self, messages: list,stream = False):
        """Send user input to the Guard service."""
        if not self.token:
            return {"error": "Authorization token not found. Please login to proceed."}
        if not self.config_id:
            return {"error": "Config ID is required. Please pick a policy."}

        headers = self._get_headers()
        payload = {"config_id": self.config_id, "messages": messages, "stream": stream}

        try:
            response = requests.post(self.guard_url, json=payload, headers=headers)
            response.raise_for_status()
            msg = response.json()
            return msg
        except RequestException as err:
            return {"error": f"Request failed: {err}"}
        except Exception as err:
            return {"error": f"An unexpected error occurred: {err}"}

    def get_base_url(self):
        """Get the current base URL."""
        return self.base_url

    def set_base_url(self, base_url: str):
        """Set a new base URL."""
        self.base_url = base_url
        self.guard_url = f"{self.base_url}/v1/chat/completions"
    
    def set_token(self,token:str):
        """Set a new token directly"""
        self.token = token


