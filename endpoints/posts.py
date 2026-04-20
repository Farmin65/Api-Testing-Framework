from endpoints.base import BaseEndpoint

class PostsEndpoint(BaseEndpoint):
    path = "posts"

    @classmethod
    def get_by_user(cls, user_id: int):
        return cls.client.get(cls.path, params={"userId": user_id})

    @classmethod
    def get_comments(cls, post_id: int):
        return cls.client.get(f"{cls.path}/{post_id}/comments")