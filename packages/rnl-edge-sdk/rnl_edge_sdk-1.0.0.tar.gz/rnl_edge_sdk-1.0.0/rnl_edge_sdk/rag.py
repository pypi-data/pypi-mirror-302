from .exceptions.rnl_edge_client_exception import RnlEdgeClientException

class RnlEdgeRag:
    def __init__(self, session, environment):
        self.session = session
        self.environment = environment
        self.access_token = None
        
    def auth(self, auth_type, credentials):
        url = f"{self.environment.host.value}/auth"
        data = {
            "authType": auth_type,
            "credentials": credentials
        }
        response = self.session.post(url, json=data)
        if response.status_code == 200:
            auth_data = response.json()
            self.access_token = auth_data.get('accessToken')
            self.session.headers.update({"x-rnledge-token": self.access_token})
            return auth_data
        else:
            raise RnlEdgeClientException(f"Authentication failed: {response.text}")

    def logout(self, auth_type):
        url = f"{self.environment.host.value}/logout"
        data = {"authType": auth_type}
        response = self.session.post(url, json=data)
        if response.status_code == 200:
            return response.text
        else:
            raise RnlEdgeClientException(f"Failed to logout: {response.text}")
      
    def rag_query(self, query, categories=None):
        url = f"{self.environment.host.value}/rag/query"
        data = {
            "query": query,
            "categories": categories or []
        }
        response = self.session.post(url, json=data)
        if response.status_code == 200:
            return response.json()
        else:
            raise RnlEdgeClientException(f"Failed to query rag: {response.text}")
        
    def rag_search_documents(self, query, docType=[]):
        url = f"{self.environment.host.value}/rag/searchDocuments"
        data = {
            "query": query,
            "categories": docType or []
        }
        response = self.session.post(url, json=data)
        if response.status_code == 200:
            return response.json()
        else:
            raise RnlEdgeClientException(f"Failed to search documents: {response.text}")
        
    def rag_generate(self, query, context, conversation=[], params={}):
        url = f"{self.environment.host.value}/rag/generate"
        data = {
            "query": query,
            "context": context,
            "conversation": conversation or [],
            "params": params or {}
        }
        response = self.session.post(url, json=data)
        if response.status_code == 200:
            return response.json()
        else:
            raise RnlEdgeClientException(f"Failed to generate rag: {response.text}")
