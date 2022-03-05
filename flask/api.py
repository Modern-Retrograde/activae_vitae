from models import Event
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


class SuccessResponse(BaseResponse):
    def __init__(self, **kwargs):
        super(SuccessResponse, self).__init__(200, **kwargs)


class OneOrMoreParamsMissedError(ErrorResponse):
    def __init__(self):
        super(OneOrMoreParamsMissedError, self).__init__(400, "One or more params are missed")


class WrongDateEntered(ErrorResponse):
    def __init__(self):
        super(WrongDateEntered, self).__init__(400, "Date format is wrong. Follow this: " + date_format)


class TooLongEventName(ErrorResponse):
    def __init__(self, maximum: int):
        super(TooLongEventName, self).__init__(400, "Too long name for the event, max: " + str(maximum))


class WrongPasswordOrEmail(ErrorResponse):
    def __init__(self):
        super(WrongPasswordOrEmail, self).__init__(403, "Wrong email or password")


class RegistrationError(ErrorResponse):
    def __init__(self, error_text: str):
        super(RegistrationError, self).__init__(400, error_text)


class Unauthorized(ErrorResponse):
    def __init__(self):
        super(Unauthorized, self).__init__(401, "Unauthorized")


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
            "short_description": self.event.short_description,
            "photos": list(map(lambda x: x.link, self.photos))
        }
        response["event"] = event
        return response
