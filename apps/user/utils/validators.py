from django.core.validators import RegexValidator


class PhoneNumberValidator(RegexValidator):
    def __init__(self):
        self.regex = r'^09\d{9}$'
        self.message = "The phone number is not valid. The phone number must start with 091 or similar and contain 11 digits."
        self.code = 'invalid_phone_number'
        super().__init__(regex=self.regex, message=self.message, code=self.code)
