# api_client.py
import requests
import logging

class APIClient:
    def __init__(self, base_url, user_api_key, user_email):
        self.base_url = base_url
        self.user_api_key = user_api_key
        self.user_email = user_email
        logging.basicConfig(level=logging.DEBUG)

    def post(self, endpoint, json_data=None):
        headers = {
            'Content-Type': 'application/json',
            'x-api-key': self.user_api_key,
            'x-email': self.user_email
        }
        url = f'{self.base_url}/{endpoint}'
        #logging.debug(f'Posting to {url} with headers {headers} and json {json_data}')
        try:
            response = requests.post(url, headers=headers, json=json_data)
            response.raise_for_status()
            #logging.debug(f'Response: {response.status_code} {response.text}')
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            logging.error(f'HTTP error occurred: {http_err}')
            logging.error(f'Response content: {response.content}')
            raise
        except Exception as err:
            logging.error(f'Other error occurred: {err}')
            raise
