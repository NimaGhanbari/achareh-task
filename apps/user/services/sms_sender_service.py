from achareh_project.settings import KAVENEGAR_APP


def send_verification_sms(message_body, recipient_number):
    params = {
        'receptor': recipient_number,
        'token': message_body,
        'type': 'sms',
    }
    response = KAVENEGAR_APP.verify_lookup(params)
    return response
