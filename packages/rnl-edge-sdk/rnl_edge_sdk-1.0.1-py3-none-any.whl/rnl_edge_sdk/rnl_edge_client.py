import requests
from .auth import RnlEdgeAuth
from .others import RnlEdgeOthers
from .documents import RnlEdgeDocuments
from .rag import RnlEdgeRag
from .prompt import RnlEdgePrompt
from .feedback import RnlEdgeFeedback
from .compass import RnlEdgeCompass

class RnlEdgeClient:
    def __init__(self, environment, api_key, org_subdomain):
        self.environment = environment
        self.api_key = api_key
        self.org_subdomain = org_subdomain
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.api_key}",
            "x-org-subdomain": self.org_subdomain,
            "Content-Type": "application/json",
            "User-Agent": "RnlEdgeSDK/1.0.0",
            "Accept": "*/*",
        })
        self.auth = RnlEdgeAuth(self.session, self.environment)
        self.others = RnlEdgeOthers(self.session, self.environment)
        self.documents = RnlEdgeDocuments(self.session, self.environment)
        self.rag = RnlEdgeRag(self.session, self.environment)
        self.prompt = RnlEdgePrompt(self.session, self.environment)
        self.feedback = RnlEdgeFeedback(self.session, self.environment)
        self.compass = RnlEdgeCompass(self.session, self.environment)
