# Этот модуль предназначен для описания всех ошибок.
class UserErrors(BaseException):
    def __init__(self,  comment: str, code: int = 400):
        self.code = code
        self.comment = comment
        super(UserErrors, self).__init__((f"User's error [{self.code}]: {comment}", ))

    def __bool__(self):
        return False


class EventError(BaseException):
    def __init__(self, comment: str, code: int = 500):
        self.code = code
        self.comment = comment
        super(EventError, self).__init__((f"Event's error [{self.code}]: {self.comment}", ))


class EmailAlreadyUsedError(UserErrors):
    def __init__(self, email: str, ):
        super(EmailAlreadyUsedError, self).__init__(f"Почта '{email}' уже занята.", 400)
