""" Adapters """
import requests
from openai import OpenAI
from dotenv import dotenv_values
from models.filer import Filer

class OpenRouterApi:
    """ Open Router Api """
    def __init__(self) -> None:
        dov = dotenv_values('models/.env')
        self.api_key = dov['APIKEY']
        self.client = OpenAI(
                    base_url=dov["ENDPOINT"],
                    api_key=self.api_key,
                    )
        self.models_list_endpoint = dov["OPENROUTERMODELS"]

    def get_answer(self, context: dict) -> str:
        """ Get answer """
        completion = self.client.chat.completions.create(
                                        model=context["model"],
                                        messages=context["messages"]
                                )
        return str(completion.choices[0].message.content)

    def get_models(self) -> None:
        """ Get available models """
        headers = {"Authorization": f"Bearer {self.api_key}"}
        response = requests.get(
                            url=self.models_list_endpoint,      # type: ignore
                            headers=headers,
                            timeout=5
                            )
        Filer('results/models.json').saveDictAsJson(response.json())
        return response.json()
