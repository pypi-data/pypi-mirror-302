from .exceptions.rnl_edge_client_exception import RnlEdgeClientException

class RnlEdgePrompt:
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
      
    def get_prompt_history(self):
        url = f"{self.environment.host.value}/prompt/history"
        response = self.session.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            raise RnlEdgeClientException(f"Failed to get prompt history: {response.text}")
        
    def save_prompt(self, prompt, summarizedPrompt=None, category=[]):
        url = f"{self.environment.host.value}/prompt/save"
        data = {
            "category": category,
            "prompt": prompt,
            "summarizedPrompt": summarizedPrompt
        }
        response = self.session.post(url, json=data)
        if response.status_code == 200:
            return response.json()
        else:
            raise RnlEdgeClientException(f"Failed to save prompt: {response.text}")
        
    def update_prompt(self, promptId, prompt, summarizedPrompt=None, category=[]):
        url = f"{self.environment.host.value}/prompt/update"
        data = {
            "category": category,
            "prompt": prompt,
            "summarizedPrompt": summarizedPrompt
        }
        response = self.session.put(f"{url}/{promptId}", json=data)
        if response.status_code == 200:
            return response.json()
        else:
            raise RnlEdgeClientException(f"Failed to update prompt: {response.text}")
    
    def delete_prompt(self, promptId):
        url = f"{self.environment.host.value}/prompt/delete"
        response = self.session.delete(f"{url}/{promptId}")
        if response.status_code == 200:
            return response.status_code
        else:
            raise RnlEdgeClientException(f"Failed to delete prompt: {response.text}")
        
    def delete_all_prompts(self):
        url = f"{self.environment.host.value}/prompt/deleteAll"
        response = self.session.delete(url)
        if response.status_code == 200:
            return response.status_code
        else:
            raise RnlEdgeClientException(f"Failed to delete all prompts: {response.text}")