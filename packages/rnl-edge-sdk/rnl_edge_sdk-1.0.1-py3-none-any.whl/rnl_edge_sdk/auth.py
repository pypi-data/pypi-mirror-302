from .exceptions.rnl_edge_client_exception import RnlEdgeClientException
from .responses.get_member_orgs_response import GetMemberOrgsResponse

class RnlEdgeAuth:
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
        
    def get_auth_types(self):
        url = f"{self.environment.host.value}/authTypes"
        response = self.session.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            raise RnlEdgeClientException(f"Failed to get auth types: {response.text}")

    def generate_password_token(self, data):
        url = f"{self.environment.host.value}/generatePasswordToken"
        response = self.session.post(url, json=data)
        if response.status_code == 200:
            return response.status_code
        else:
            raise RnlEdgeClientException(f"Failed to generate password token: {response.text}")
        
    def set_new_password(self, auth_type, credentials):
        url = f"{self.environment.host.value}/setNewPassword"
        data = {
            "authType": auth_type,
            "credentials": credentials
        }
        response = self.session.post(url, json=data)
        if response.status_code == 200:
            return response.status_code
        else:
            raise RnlEdgeClientException(f"Failed to set new password: {response.text}")

    def check_password_token(self, auth_type, credentials):
        url = f"{self.environment.host.value}/checkPasswordResetTokenIsValid"
        data = {
            "authType": auth_type,
            "credentials": credentials
        }
        response = self.session.post(url, json=data)
        if response.status_code == 200:
            return response.status_code
        else:
            raise RnlEdgeClientException(f"Failed to check password token: {response.text}")

    def get_member_orgs(self, email):
        url = f"{self.environment.host.value}/getMemberOrgs/{email}"
        response = self.session.get(url)
        if response.status_code == 200:
            return GetMemberOrgsResponse.from_dict(response.json())
        else:
            raise RnlEdgeClientException(f"Failed to get member orgs: {response.text}")
        
    def logout(self, auth_type):
        url = f"{self.environment.host.value}/logout"
        data = {"authType": auth_type}
        response = self.session.post(url, json=data)
        if response.status_code == 200:
            return response.text
        else:
            raise RnlEdgeClientException(f"Failed to logout: {response.text}")
