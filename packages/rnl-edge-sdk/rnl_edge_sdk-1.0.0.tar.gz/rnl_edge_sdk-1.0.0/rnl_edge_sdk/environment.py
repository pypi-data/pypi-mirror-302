from enum import Enum

class Environment:
    class Hosts(Enum):
        PRODUCTION = "https://api.rnledge.ai"
        SANDBOX = "https://sandbox-api.rnledge.ai"
        QA = "https://qa-api.rnledge.ai"
        LOCAL = "http://localhost:9000"

    def __init__(self, host, name):
        self.host = host
        self.name = name