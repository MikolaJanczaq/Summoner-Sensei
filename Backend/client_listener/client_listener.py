import os

import requests
import urllib3
from dotenv import load_dotenv

# Ignore warning about insecure request (InsecureRequestWarning)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

load_dotenv()

game_data_endpoint = os.getenv("LIVE_CLIENT_SERVER")

def get_client_data():
    # Using verify=False because the League of Legends client API uses a self-signed certificate
    client_response = requests.get(game_data_endpoint, verify=False)
    return client_response.json()
