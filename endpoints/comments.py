from endpoints.base import BaseEndpoint

class CommentsEndpoint(BaseEndpoint):
    path = "comments"

    @classmethod
    def get_by_post(cls, post_id: int):
        return cls.client.get(cls.path, params={"postId": post_id})