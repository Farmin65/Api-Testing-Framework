import pytest
from core.assertions import APIAssertions

class TestCommentsAPI:
    
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_get_all_comments(self, comments_endpoint):
        response = comments_endpoint.get_list()
        
        comments_endpoint.assertions.assert_status_code(response, 200)
        comments_endpoint.assertions.assert_list_not_empty(response)
        comments_endpoint.assertions.assert_json_contains(response, "id")
        comments_endpoint.assertions.assert_json_contains(response, "postId")
        comments_endpoint.assertions.assert_json_contains(response, "email")

    @pytest.mark.regression
    def test_get_single_comment(self, comments_endpoint):
        comment_id = 1
        response = comments_endpoint.get_by_id(comment_id)
        
        comments_endpoint.assertions.assert_status_code(response, 200)
        comments_endpoint.assertions.assert_json_value(response, "id", comment_id)
        
        json_data = response.json()
        assert "postId" in json_data
        assert "name" in json_data
        assert "email" in json_data
        assert "body" in json_data

    @pytest.mark.regression
    def test_filter_comments_by_post(self, comments_endpoint):
        post_id = 1
        response = comments_endpoint.get_by_post(post_id)
        
        comments_endpoint.assertions.assert_status_code(response, 200)
        comments_endpoint.assertions.assert_list_not_empty(response)
        
        comments = response.json()
        for comment in comments:
            assert comment["postId"] == post_id

    @pytest.mark.smoke
    @pytest.mark.regression
    def test_create_comment(self, comments_endpoint, test_data):
        payload = test_data.generate_comment(post_id=1)
        response = comments_endpoint.create(**payload)
        
        comments_endpoint.assertions.assert_status_code(response, 201)
        
        json_data = response.json()
        assert json_data["postId"] == payload["postId"]
        assert json_data["name"] == payload["name"]
        assert json_data["email"] == payload["email"]
        assert json_data["body"] == payload["body"]
        assert "id" in json_data

    @pytest.mark.regression
    def test_update_comment_put(self, comments_endpoint, test_data):
        comment_id = 1
        payload = test_data.generate_comment(post_id=2)
        
        response = comments_endpoint.update(comment_id, **payload)
        
        comments_endpoint.assertions.assert_status_code(response, 200)
        
        json_data = response.json()
        assert json_data["id"] == comment_id
        assert json_data["body"] == payload["body"]

    @pytest.mark.regression
    def test_update_comment_patch(self, comments_endpoint):
        comment_id = 1
        payload = {"body": "This comment has been patched with new content."}
        
        response = comments_endpoint.patch(comment_id, **payload)
        
        comments_endpoint.assertions.assert_status_code(response, 200)
        assert response.json()["body"] == payload["body"]

    @pytest.mark.regression
    def test_delete_comment(self, comments_endpoint, test_data):
        create_payload = test_data.generate_comment(post_id=1)
        create_response = comments_endpoint.create(**create_payload)
        comment_id = create_response.json()["id"]
        
        delete_response = comments_endpoint.delete(comment_id)
        comments_endpoint.assertions.assert_status_code(delete_response, 200)
        
        get_response = comments_endpoint.get_by_id(comment_id)
        comments_endpoint.assertions.assert_status_code(get_response, 404)