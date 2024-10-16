from .exceptions.rnl_edge_client_exception import RnlEdgeClientException

class RnlEdgeCompass:
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
      
    def get_email_verification_code(self, email):
        url = f"{self.environment.host.value}/emailVerification/generate"
        data = {"email": email}
        response = self.session.post(url, json=data)
        if response.status_code == 200:
            return response.json()
        else:
            raise RnlEdgeClientException(f"Failed to get email verification code: {response.text}")
        
    def verify_email(self, email, code):
        url = f"{self.environment.host.value}/emailVerification/verify/{email}/{code}"
        response = self.session.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            raise RnlEdgeClientException(f"Failed to verify email: {response.text}")