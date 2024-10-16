from enum import Enum

class Endpoint:
    class Style(Enum):
        PERSON = "PERSON"
        EVENT = "EVENT"

    def __init__(self, url, destination_object, style, extra_fields=None):
        self.url = url
        self.destination_object = destination_object
        self.style = style
        self.extra_fields = extra_fields or []

    class ExtraField:
        def __init__(self, name, type):
            self.name = name
            self.type = type