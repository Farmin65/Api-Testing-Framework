import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import logging
from typing import Optional, Dict, Any
from config.settings import settings
from utils.logger import setup_logger

logger = setup_logger(__name__)

class APIClient:
    def __init__(self):
        self.base_url = settings.BASE_URL.rstrip('/')
        self.session = requests.Session()
        self._configure_retries()
        self._configure_headers()

    def _configure_retries(self):
        retry_strategy = Retry(
            total=settings.RETRY_COUNT,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS", "POST", "PUT", "DELETE", "PATCH"]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

    def _configure_headers(self):
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json"
        })

    def _log_request(self, method: str, url: str, **kwargs):
        logger.info(f"Request: {method} {url}")
        if 'json' in kwargs:
            logger.debug(f"Payload: {kwargs['json']}")

    def _log_response(self, response: requests.Response):
        logger.info(f"Response: {response.status_code} {response.reason}")
        if response.content:
            logger.debug(f"Body: {response.text[:500]}")

    def request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        timeout = kwargs.pop('timeout', settings.API_TIMEOUT)
        
        self._log_request(method, url, **kwargs)
        
        response = self.session.request(
            method=method,
            url=url,
            timeout=timeout,
            **kwargs
        )
        
        self._log_response(response)
        return response

    def get(self, endpoint: str, **kwargs) -> requests.Response:
        return self.request("GET", endpoint, **kwargs)

    def post(self, endpoint: str, **kwargs) -> requests.Response:
        return self.request("POST", endpoint, **kwargs)

    def put(self, endpoint: str, **kwargs) -> requests.Response:
        return self.request("PUT", endpoint, **kwargs)

    def patch(self, endpoint: str, **kwargs) -> requests.Response:
        return self.request("PATCH", endpoint, **kwargs)

    def delete(self, endpoint: str, **kwargs) -> requests.Response:
        return self.request("DELETE", endpoint, **kwargs)