from faker import Faker
import random

fake = Faker()

class TestDataGenerator:
    
    @staticmethod
    def generate_post(user_id: int = None) -> dict:
        return {
            "userId": user_id or random.randint(1, 10),
            "title": fake.sentence(nb_words=6),
            "body": fake.paragraph(nb_sentences=3)
        }

    @staticmethod
    def generate_user() -> dict:
        return {
            "name": fake.name(),
            "username": fake.user_name(),
            "email": fake.email(),
            "address": {
                "street": fake.street_name(),
                "suite": fake.secondary_address(),
                "city": fake.city(),
                "zipcode": fake.zipcode(),
                "geo": {
                    "lat": str(fake.latitude()),
                    "lng": str(fake.longitude())
                }
            },
            "phone": fake.phone_number(),
            "website": fake.url(),
            "company": {
                "name": fake.company(),
                "catchPhrase": fake.catch_phrase(),
                "bs": fake.bs()
            }
        }

    @staticmethod
    def generate_comment(post_id: int = None) -> dict:
        return {
            "postId": post_id or random.randint(1, 100),
            "name": fake.sentence(nb_words=3),
            "email": fake.email(),
            "body": fake.paragraph(nb_sentences=2)
        }