from .exceptions.rnl_edge_client_exception import RnlEdgeClientException
from .responses.get_documents_response import GetDocumentsResponse
from .responses.post_document_response import PostDocumentResponse

class RnlEdgeDocuments:
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
      
    def get_documents(self):
        if not self.access_token:
            raise RnlEdgeClientException("Not authenticated. Please call auth() method first.")

        url = f"{self.environment.host.value}/documents"
        headers = {
            "x-rnledge-token": self.access_token,
        }
        response = self.session.get(url, headers=headers)
        
        if response.status_code == 200:
            return GetDocumentsResponse.from_dict(response.json())
        else:
            raise RnlEdgeClientException(f"Failed to get documents: {response.text}")

    def post_document(self, request):
        url = f"{self.environment.host.value}/documents"
        response = self.session.post(url, json=request.to_dict())
        if response.status_code == 200:
            return PostDocumentResponse.from_dict(response.json())
        else:
            raise RnlEdgeClientException(f"Failed to post document: {response.text}")
        
    def delete_document(self, document_id):
        url = f"{self.environment.host.value}/document/{document_id}"
        response = self.session.delete(url)
        if response.status_code == 200:
            return response.text
        else:
            raise RnlEdgeClientException(f"Failed to delete document: {response.text}")
        
    def get_document_details(self, document_id):
        url = f"{self.environment.host.value}/document/{document_id}"
        response = self.session.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            raise RnlEdgeClientException(f"Failed to get document details: {response.text}")
        
    def get_file(self, document_id):
        url = f"{self.environment.host.value}/file/{document_id}"
        response = self.session.get(url)
        if response.status_code == 200:
            return response.content
        else:
            raise RnlEdgeClientException(f"Failed to get file: {response.text}")
        
    def delete_multiple_documents(self, data):
        url = f"{self.environment.host.value}/documents/deleteMultiple"
        response = self.session.delete(url, json=data)
        if response.status_code == 200:
            return response.text
        else:
            raise RnlEdgeClientException(f"Failed to delete multiple documents: {response.text}")
        
    def get_document_categories(self):
        url = f"{self.environment.host.value}/categories"
        response = self.session.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            raise RnlEdgeClientException(f"Failed to get document categories: {response.text}")
