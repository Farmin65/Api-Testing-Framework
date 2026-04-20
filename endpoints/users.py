from endpoints.base import BaseEndpoint

class UsersEndpoint(BaseEndpoint):
    path = "users"

    @classmethod
    def get_by_username(cls, username: str):
        return cls.client.get(cls.path, params={"username": username})