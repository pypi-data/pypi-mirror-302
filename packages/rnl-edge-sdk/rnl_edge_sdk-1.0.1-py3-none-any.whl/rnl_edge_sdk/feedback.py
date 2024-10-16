from .exceptions.rnl_edge_client_exception import RnlEdgeClientException

class RnlEdgeFeedback:
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
      
    def get_feedback(self, requestId):
        url = f"{self.environment.host.value}/rag/feedback/{requestId}"
        response = self.session.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            raise RnlEdgeClientException(f"Failed to get feedback: {response.text}")
        
    def save_feedback(self, requestId, type, feedback, documentId=None, chunkId=None, prompt=None, chatResponse=None):
        url = f"{self.environment.host.value}/rag/feedback"
        data = {
            "requestId": requestId,
            "type": type,
            "feedback": feedback,
            "documentId": documentId,
            "chunkId": chunkId,
            "prompt": prompt,
            "chatResponse": chatResponse
        }
        response = self.session.put(url, json=data)
        if response.status_code == 200:
            return response.json()
        else:
            raise RnlEdgeClientException(f"Failed to save feedback: {response.text}")
        
    def delete_feedback(self, feedbackId):
        url = f"{self.environment.host.value}/rag/feedback/{feedbackId}"
        response = self.session.delete(url)
        if response.status_code == 200:
            return response.status_code
        else:
            raise RnlEdgeClientException(f"Failed to delete feedback: {response.text}")