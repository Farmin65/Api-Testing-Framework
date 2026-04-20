from requests import Response
from typing import Optional, List, Dict, Any


class APIAssertions:

    @staticmethod
    def assert_status_code(response: Response, expected_code: int):
        assert response.status_code == expected_code, \
            f"Expected status code {expected_code}, got {response.status_code}. Response: {response.text[:200]}"

    @staticmethod
    def assert_json_contains(response: Response, key: str):
        json_data = response.json()
        if isinstance(json_data, list):
            assert all(key in item for item in json_data), f"Key '{key}' not found in all list elements"
        else:
            assert key in json_data, f"Key '{key}' not found in response"

    @staticmethod
    def assert_json_value(response: Response, key: str, expected_value: Any):
        json_data = response.json()
        if isinstance(json_data, list):
            actual_values = [item.get(key) for item in json_data]
            assert expected_value in actual_values, f"Value '{expected_value}' not found in list for key '{key}'"
        else:
            actual_value = json_data.get(key)
            assert actual_value == expected_value, \
                f"Expected '{key}' to be '{expected_value}', got '{actual_value}'"

    @staticmethod
    def assert_response_time(response: Response, max_ms: int):
        assert response.elapsed.total_seconds() * 1000 < max_ms, \
            f"Response time {response.elapsed.total_seconds() * 1000:.2f}ms exceeds {max_ms}ms"

    @staticmethod
    def assert_list_not_empty(response: Response):
        json_data = response.json()
        assert isinstance(json_data, list), "Response is not a list"
        assert len(json_data) > 0, "Response list is empty"