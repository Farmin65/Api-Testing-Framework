import pytest
from core.models import User, Post, Comment
from pydantic import ValidationError
from typing import List

class TestSchemaValidation:
    
    @pytest.mark.regression
    def test_user_schema_validation(self, users_endpoint):
        response = users_endpoint.get_list()
        users = response.json()
        
        for user_data in users[:5]:
            try:
                User(**user_data)
            except ValidationError as e:
                pytest.fail(f"User schema validation failed: {e}")

    @pytest.mark.regression
    def test_post_schema_validation(self, posts_endpoint):
        response = posts_endpoint.get_list()
        posts = response.json()
        
        for post_data in posts[:5]:
            try:
                Post(**post_data)
            except ValidationError as e:
                pytest.fail(f"Post schema validation failed: {e}")

    @pytest.mark.regression
    def test_comment_schema_validation(self, comments_endpoint):
        response = comments_endpoint.get_list()
        comments = response.json()
        
        for comment_data in comments[:5]:
            try:
                Comment(**comment_data)
            except ValidationError as e:
                pytest.fail(f"Comment schema validation failed: {e}")