# Этот модуль предназначен для описания всех ошибок.
class ClassicError(BaseException):
    def __init__(self, comment: str):
        super(ClassicError, self).__init__((comment, ))


class UserErrors(ClassicError):
    def __init__(self, comment: str):
        super(UserErrors, self).__init__("User's error: " + comment)


class EventError(ClassicError):
    def __init__(self, comment: str):
        super(EventError, self).__init__("Event's error: " + comment)


class EmailAlreadyUsedError(UserErrors):
    def __init__(self, email: str):
        super(EmailAlreadyUsedError, self).__init__(f"Email '{email}' already used.")


class EventPhotoNotFoundError(EventError):
    def __init__(self, event_id: int, link: str):
        super(EventPhotoNotFoundError, self).__init__(f"No photo for event {event_id}.\nLink: '{link}'")


class SavedEventNotFoundError(EventError):
    def __init__(self, event_id: int, user_id: int):
        super(SavedEventNotFoundError, self).__init__(f"No saved event (ID {event_id}) found for user (ID {user_id}.")


class EventsFormNotFoundError(EventError):
    def __init__(self, event_form_id: int):
        super(EventsFormNotFoundError, self).__init__(f"No event's form (ID {event_form_id}) found.")
