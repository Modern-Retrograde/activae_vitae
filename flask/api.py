from models import Event, EventComment
from configs import date_format


class BaseResponse:
    def __init__(self, code: int, **kwargs):
        self.code = code
        self.response_dict = kwargs

    def __dict__(self):
        response = {"code": self.code}
        for key, value in self.response_dict.items():
            response[key] = value
        return response


class ErrorResponse(BaseResponse):
    def __init__(self, error_code: int, error_text: str):
        super(ErrorResponse, self).__init__(error_code, error=error_text)


class NotFound(BaseResponse):
    def __init__(self):
        super(NotFound, self).__init__(404)


class RoleNotFound(ErrorResponse):
    def __init__(self, role: str):
        super(RoleNotFound, self).__init__(404, f"Role '{role}' not found.")


class SuccessResponse(BaseResponse):
    def __init__(self, **kwargs):
        super(SuccessResponse, self).__init__(200, **kwargs)


class BusyEmailError(ErrorResponse):
    def __init__(self):
        super(BusyEmailError, self).__init__(400, "This email is busy.")


class OneOrMoreParamsMissedError(ErrorResponse):
    def __init__(self, missed_params: list = None):
        if missed_params:
            text = "Missed params: " + ", ".join(map(lambda x: f"'{x}'", missed_params))
        else:
            text = "One or more params are missed."
        super(OneOrMoreParamsMissedError, self).__init__(400, text)


class WrongDateEntered(ErrorResponse):
    def __init__(self):
        super(WrongDateEntered, self).__init__(400, "Date format is wrong. Follow this: " + date_format)


class TooLongEventName(ErrorResponse):
    def __init__(self, maximum: int):
        super(TooLongEventName, self).__init__(400, "Too long name for the event, max: " + str(maximum))


class AccountWasDeleted(ErrorResponse):
    def __init__(self):
        super(AccountWasDeleted, self).__init__(500, "Account was deleted. Please re-login.")


class WrongPasswordOrEmail(ErrorResponse):
    def __init__(self):
        super(WrongPasswordOrEmail, self).__init__(403, "Wrong email or password")


class RegistrationError(ErrorResponse):
    def __init__(self, error_text: str):
        super(RegistrationError, self).__init__(400, error_text)


class Unauthorized(ErrorResponse):
    def __init__(self):
        super(Unauthorized, self).__init__(401, "Unauthorized")


class ParamMustBeNum(ErrorResponse):
    def __init__(self, param_name: str):
        super(ParamMustBeNum, self).__init__(400, f"'{param_name}' param must be num.")


class EventsResponse(BaseResponse):
    def __init__(self, events: list):
        super(EventsResponse, self).__init__(code=200)
        self.events = events

    def __dict__(self):
        response = super(EventsResponse, self).__dict__()
        events = list()
        event: Event
        for event, is_saved in self.events:
            events.append({
                "id": event.id,
                "name": event.name,
                "short_description": event.short_description,
                "format": event.event_format,
                "date": event.event_date.strftime(date_format),
                "is_saved": bool(is_saved)
            })
        response["events"] = events
        return response


class EventResponse(BaseResponse):
    def __init__(self, event):
        super(EventResponse, self).__init__(200)
        self.event = event["event"]
        self.photos = event["photos"]

    def __dict__(self):
        response = super(EventResponse, self).__dict__()

        event = {
            "id": self.event.id,
            "date": self.event.event_date.strftime(date_format),
            "name": self.event.name,
            "format": self.event.event_format,
            "short_description": self.event.short_description,
            "description": self.event.description,
            "photos": list(map(lambda x: x.link, self.photos))
        }
        response["event"] = event
        return response


class UserResponse(BaseResponse):
    def __init__(self, user):
        super(UserResponse, self).__init__(200)
        self.user = user

    def __dict__(self):
        response = super(UserResponse, self).__dict__()
        user = {
            "id": self.user.id,
            "role": self.user.role,
            "verified": self.user.verified,
            "email": self.user.email,
            "full_name": self.user.full_name,
        }
        response["user"] = user
        return response


class UsersResponse(BaseResponse):
    def __init__(self, users: list):
        super(UsersResponse, self).__init__(200)
        self.users = users

    def __dict__(self):
        response = super(UsersResponse, self).__dict__()
        users = [
            {
                "id": user.id,
                "role": user.role,
                "verified": user.verified,
                "email": user.email,
                "full_name": user.full_name,
            }
            for user in self.users
        ]
        response["users"] = users
        return response


class CommentsResponse(BaseResponse):
    def __init__(self, comments: list):
        super(CommentsResponse, self).__init__(200)
        self.comments = comments

    def __dict__(self):
        response = super(CommentsResponse, self).__dict__()
        comment: EventComment
        comments = [
            {
                "id": comment.id,
                "event_id": comment.event_id,
                "text": comment.text,
                "user_id": comment.user_id
            }
            for comment in self.comments
        ]
        response["comments"] = comments

        return response
