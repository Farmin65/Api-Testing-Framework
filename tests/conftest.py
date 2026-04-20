import sys
import os

import pytest
from core.client import APIClient
from endpoints.posts import PostsEndpoint
from endpoints.users import UsersEndpoint
from endpoints.comments import CommentsEndpoint
from utils.data_generator import TestDataGenerator

@pytest.fixture(scope="session")
def api_client():
    return APIClient()

@pytest.fixture(scope="session")
def posts_endpoint():
    return PostsEndpoint()

@pytest.fixture(scope="session")
def users_endpoint():
    return UsersEndpoint()

@pytest.fixture(scope="session")
def comments_endpoint():
    return CommentsEndpoint()

@pytest.fixture
def test_data():
    return TestDataGenerator()

@pytest.fixture
def create_test_post(posts_endpoint, test_data):
    def _create_post(user_id=None):
        payload = test_data.generate_post(user_id)
        response = posts_endpoint.create(**payload)
        return response.json()
    return _create_post

@pytest.fixture
def cleanup_post(posts_endpoint):
    post_ids = []
    yield post_ids
    for post_id in post_ids:
        posts_endpoint.delete(post_id)

def pytest_configure(config):
    config.addinivalue_line("markers", "smoke: Critical path tests")
    config.addinivalue_line("markers", "regression: Full regression suite")