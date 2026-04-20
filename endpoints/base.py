from core.client import APIClient
from core.assertions import APIAssertions

class BaseEndpoint:
    client = APIClient()
    assertions = APIAssertions()
    path: str = ""

    @classmethod
    def get_list(cls, **params):
        return cls.client.get(cls.path, params=params)

    @classmethod
    def get_by_id(cls, resource_id: int):
        return cls.client.get(f"{cls.path}/{resource_id}")

    @classmethod
    def create(cls, **data):
        return cls.client.post(cls.path, json=data)

    @classmethod
    def update(cls, resource_id: int, **data):
        return cls.client.put(f"{cls.path}/{resource_id}", json=data)

    @classmethod
    def patch(cls, resource_id: int, **data):
        return cls.client.patch(f"{cls.path}/{resource_id}", json=data)

    @classmethod
    def delete(cls, resource_id: int):
        return cls.client.delete(f"{cls.path}/{resource_id}")