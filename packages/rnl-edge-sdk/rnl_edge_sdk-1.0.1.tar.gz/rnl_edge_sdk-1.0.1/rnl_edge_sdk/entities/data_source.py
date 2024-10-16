from enum import Enum
from .endpoint import Endpoint

class DataSource:
    class Type(Enum):
        SLATE = "SLATE"
        FLAT_FILE = "FLAT_FILE"
        SALESFORCE = "SALESFORCE"

    def __init__(self, type, endpoints=None, api_key=None, api_secret=None, username=None, password=None):
        self.type = type
        self.endpoints = endpoints or []
        self.api_key = api_key
        self.api_secret = api_secret
        self.username = username
        self.password = password