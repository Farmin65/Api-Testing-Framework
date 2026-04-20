import pytest
from core.assertions import APIAssertions

class TestUsersAPI:
    
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_get_all_users(self, users_endpoint):
        response = users_endpoint.get_list()
        
        users_endpoint.assertions.assert_status_code(response, 200)
        users_endpoint.assertions.assert_list_not_empty(response)
        users_endpoint.assertions.assert_json_contains(response, "id")
        users_endpoint.assertions.assert_json_contains(response, "email")
        users_endpoint.assertions.assert_json_contains(response, "username")

    @pytest.mark.regression
    def test_get_single_user(self, users_endpoint):
        user_id = 1
        response = users_endpoint.get_by_id(user_id)
        
        users_endpoint.assertions.assert_status_code(response, 200)
        users_endpoint.assertions.assert_json_value(response, "id", user_id)
        
        json_data = response.json()
        assert "name" in json_data
        assert "email" in json_data
        assert "address" in json_data
        assert "company" in json_data

    @pytest.mark.smoke
    @pytest.mark.regression
    def test_get_nonexistent_user(self, users_endpoint):
        response = users_endpoint.get_by_id(99999)
        users_endpoint.assertions.assert_status_code(response, 404)

    @pytest.mark.regression
    def test_filter_users_by_username(self, users_endpoint):
        username = "Bret"
        response = users_endpoint.get_by_username(username)
        
        users_endpoint.assertions.assert_status_code(response, 200)
        users_endpoint.assertions.assert_list_not_empty(response)
        
        users = response.json()
        assert len(users) == 1
        assert users[0]["username"] == username

    @pytest.mark.regression
    def test_filter_users_by_nonexistent_username(self, users_endpoint):
        response = users_endpoint.get_by_username("nonexistent_username_12345")
        
        users_endpoint.assertions.assert_status_code(response, 200)
        
        users = response.json()
        assert isinstance(users, list)
        assert len(users) == 0

    @pytest.mark.regression
    def test_create_user(self, users_endpoint, test_data):
        payload = test_data.generate_user()
        response = users_endpoint.create(**payload)
        
        users_endpoint.assertions.assert_status_code(response, 201)
        
        json_data = response.json()
        assert json_data["name"] == payload["name"]
        assert json_data["username"] == payload["username"]
        assert json_data["email"] == payload["email"]
        assert "id" in json_data

    @pytest.mark.regression
    def test_update_user_put(self, users_endpoint, test_data):
        user_id = 1
        payload = test_data.generate_user()
        
        response = users_endpoint.update(user_id, **payload)
        
        users_endpoint.assertions.assert_status_code(response, 200)
        
        json_data = response.json()
        assert json_data["id"] == user_id
        assert json_data["name"] == payload["name"]
        assert json_data["username"] == payload["username"]

    @pytest.mark.regression
    def test_update_user_patch(self, users_endpoint):
        user_id = 1
        payload = {"name": "Updated Name"}
        
        response = users_endpoint.patch(user_id, **payload)
        
        users_endpoint.assertions.assert_status_code(response, 200)
        assert response.json()["name"] == payload["name"]

    @pytest.mark.regression
    def test_delete_user(self, users_endpoint, test_data):
        create_payload = test_data.generate_user()
        create_response = users_endpoint.create(**create_payload)
        user_id = create_response.json()["id"]
        
        delete_response = users_endpoint.delete(user_id)
        users_endpoint.assertions.assert_status_code(delete_response, 200)
        
        get_response = users_endpoint.get_by_id(user_id)
        users_endpoint.assertions.assert_status_code(get_response, 404)