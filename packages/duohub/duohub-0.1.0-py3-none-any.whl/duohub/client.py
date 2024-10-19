import requests
from .exceptions import APIError
from .environment import Environment

class Duohub:
    def __init__(self, api_key=None):
        self.environment = Environment(api_key)

    def query(self, query: str, memoryID: str, assisted: bool = False):
        url = self.environment.get_full_url("/memory/")
        
        params = {
            "memoryID": memoryID,
            "query": query,
            "assisted": str(assisted).lower()
        }
        
        response = requests.get(url, params=params, headers=self.environment.headers)
        
        if response.status_code != 200:
            raise APIError(f"API request failed with status code {response.status_code}: {response.text}")
        
        return response.json()