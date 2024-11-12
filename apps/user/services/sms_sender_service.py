from achareh_project.settings import KAVENEGAR_APP
from typing import Dict, Any


def send_verification_sms(message_body: str, recipient_number: str) -> Any:
    params: Dict[str, str] = {
        'receptor': recipient_number,
        'token': message_body,
        'type': 'sms',
    }
    response = KAVENEGAR_APP.verify_lookup(params)
    return response
