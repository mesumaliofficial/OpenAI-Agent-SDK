import os
from dotenv import find_dotenv, load_dotenv
import requests
import json

load_dotenv(find_dotenv())
open_router_api = os.getenv("OPEN_ROUTER_KEY")
base_url="https://openrouter.ai/api/v1"

def get_conversion_response(user_message):
    model = "meta-llama/llama-3.3-8b-instruct:free"
    response = requests.post(
        url=f"{base_url}/chat/completions",
        headers={
            "Authorization": f"Bearer {open_router_api}",
            "Content-Type": "application/json"

        },
        data=json.dumps({
            "model": model,
            "messages": [{
                "role": "user",
                "content": user_message
            }]
        }),
    )
    return response.json()['choices'][0]['message']['content']
