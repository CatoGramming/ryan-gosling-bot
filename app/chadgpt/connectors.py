from app.settings import CHAD_GPT_TOKEN
from typing import TypedDict
import requests


class ChadGptRequestTypedDict(TypedDict):
    message: str
    api_key: str


class ChadGptService:

    def __init__(self) -> None:
        self.chad_token = CHAD_GPT_TOKEN
        self.chad_url = 'https://ask.chadgpt.ru/api/public/gpt-3.5'

    def _create_payload(self, question: str) -> ChadGptRequestTypedDict:
        return ChadGptRequestTypedDict(
            message=question,
            api_key=self.chad_token
        )

    def send_to_chad_gpt(self, question: str) -> str:
        payload = self._create_payload(question=question)
        request = requests.post(
            url=self.chad_url,
            json=payload)
        data_json = request.json()
        print(data_json)

        if not data_json['is_success']:
            error = data_json['error_message']
            return f'Something went wrong {error}'

        return data_json['response']
