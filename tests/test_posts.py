import pytest
import random
from core.assertions import APIAssertions
from core.models import Post
from pydantic import ValidationError

class TestPostsCRUD:
    
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_get_all_posts(self, posts_endpoint):
        response = posts_endpoint.get_list()
        
        posts_endpoint.assertions.assert_status_code(response, 200)
        posts_endpoint.assertions.assert_list_not_empty(response)
        posts_endpoint.assertions.assert_json_contains(response, "id")
        posts_endpoint.assertions.assert_response_time(response, 2000)

    @pytest.mark.regression
    def test_get_single_post(self, posts_endpoint):
        post_id = 1
        response = posts_endpoint.get_by_id(post_id)
        
        posts_endpoint.assertions.assert_status_code(response, 200)
        posts_endpoint.assertions.assert_json_value(response, "id", post_id)

    @pytest.mark.smoke
    @pytest.mark.regression
    def test_create_post(self, posts_endpoint, test_data):
        payload = test_data.generate_post(user_id=1)
        response = posts_endpoint.create(**payload)
        
        posts_endpoint.assertions.assert_status_code(response, 201)
        
        json_data = response.json()
        assert json_data["title"] == payload["title"]
        assert json_data["body"] == payload["body"]
        assert json_data["userId"] == payload["userId"]
        assert "id" in json_data

    @pytest.mark.regression
    def test_update_post_put(self, posts_endpoint, test_data):
        post_id = 1
        payload = test_data.generate_post(user_id=2)
        
        response = posts_endpoint.update(post_id, **payload)
        
        posts_endpoint.assertions.assert_status_code(response, 200)
        
        json_data = response.json()
        assert json_data["id"] == post_id
        assert json_data["title"] == payload["title"]

    @pytest.mark.regression
    def test_update_post_patch(self, posts_endpoint):
        post_id = 1
        payload = {"title": "Partially Updated Title"}
        
        response = posts_endpoint.patch(post_id, **payload)
        
        posts_endpoint.assertions.assert_status_code(response, 200)
        assert response.json()["title"] == payload["title"]

    @pytest.mark.smoke
    @pytest.mark.regression
    def test_delete_post(self, posts_endpoint, test_data):
        create_payload = test_data.generate_post()
        create_response = posts_endpoint.create(**create_payload)
        post_id = create_response.json()["id"]
        
        delete_response = posts_endpoint.delete(post_id)
        posts_endpoint.assertions.assert_status_code(delete_response, 200)
        
        get_response = posts_endpoint.get_by_id(post_id)
        posts_endpoint.assertions.assert_status_code(get_response, 404)

    @pytest.mark.regression
    def test_filter_posts_by_user(self, posts_endpoint):
        user_id = 1
        response = posts_endpoint.get_by_user(user_id)
        
        posts_endpoint.assertions.assert_status_code(response, 200)
        posts_endpoint.assertions.assert_list_not_empty(response)
        
        posts = response.json()
        for post in posts:
            assert post["userId"] == user_id

    @pytest.mark.regression
    def test_get_post_comments(self, posts_endpoint):
        post_id = 1
        response = posts_endpoint.get_comments(post_id)
        
        posts_endpoint.assertions.assert_status_code(response, 200)
        posts_endpoint.assertions.assert_list_not_empty(response)