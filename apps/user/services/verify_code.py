from achareh_project.settings import redis_client


def verify_code(phone_number, verification_code):

    stored_code = redis_client.get(phone_number)
    if stored_code and stored_code.decode() == verification_code:
        return True
    return False
