import urllib3
urllib3.disable_warnings()
import warnings
from urllib3.exceptions import InsecureRequestWarning, NotOpenSSLWarning

warnings.filterwarnings("ignore", category=NotOpenSSLWarning)
warnings.filterwarnings("ignore", category=InsecureRequestWarning)

import logging
logging.getLogger("urllib3").setLevel(logging.ERROR)


import requests
import json
import os
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import sys
from apikey import HomeAssistant_URL_IP, HomeAssistant_Token



class HomeAssistant:
    def __init__(self, url, token):
        self.url = url
        self.token = token
        self.session = self.requests_retry_session()
        self.easy_name_map = self.load_easy_name_map()

    @staticmethod
    def requests_retry_session(retries=3, backoff_factor=0.3, status_forcelist=(500, 502, 504), session=None):
        session = session or requests.Session()
        retry = Retry(total=retries, read=retries, connect=retries, backoff_factor=backoff_factor, status_forcelist=status_forcelist)
        adapter = HTTPAdapter(max_retries=retry)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        return session

    def call_service(self, domain, service, data):
        headers = {"Authorization": "Bearer " + self.token, "content-type": "application/json"}
        response = self.session.post(f"{self.url}/api/services/{domain}/{service}", headers=headers, json=data)
        return response.json()

    def control_light_by_name(self, easy_name, action):
        print(f"[Miles is turning {easy_name} {action}]")
        if easy_name not in self.easy_name_map:
            print(f"Error: No light found for easy name '{easy_name}'.")
            return "Error: No light found."
    
        entity_id = self.easy_name_map[easy_name]
        service = "turn_on" if action == "on" else "turn_off"
        data = {"entity_id": entity_id}
        response = self.call_service("light", service, data)

        try:
            # Get details from Home Assistant and format them as a string
            if response and isinstance(response, list) and response[0].get('state') == action:
                state_info = "successfully turned on" if action == "on" else "successfully turned off"
            else:
                state_info = "failed to turn on" if action == "on" else "failed to turn off"
        except Exception as e:
            print(f"Error processing response: {e}")
            state_info = "encountered an error while processing the response"

        formatted_message = f"{easy_name} was {state_info}."
        return formatted_message

    def load_easy_name_map(self):
        file_path = os.path.join(os.path.dirname(__file__), 'HomeAssistantDevices.json')
        try:
            with open(file_path, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"File not found: {file_path}")
            return {}
        except json.JSONDecodeError:
            print(f"Error decoding JSON from file: {file_path}")
            return {}
        
    def print_entities(self):
        headers = {"Authorization": "Bearer " + self.token, "Content-Type": "application/json"}
        response = self.session.get(f"{self.url}/api/states", headers=headers)
        if response.status_code == 200:
            entities = response.json()
            filtered_entities = []  # Prepare a list to hold filtered entities
            for entity in entities:
                if entity['entity_id'].startswith('light.') or entity['entity_id'].startswith('switch.'):
                    # Instead of printing directly, append the entity to the list
                    filtered_entities.append(entity)
            # After the loop, print the entire list as JSON
            print(json.dumps(filtered_entities, indent=4))  # Pretty print with 4-space indentation
        else:
            print("Failed to fetch entities.")


home_assistant = HomeAssistant(HomeAssistant_URL_IP, HomeAssistant_Token)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--entity-mode":
        home_assistant.print_entities()
