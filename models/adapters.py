""" Adapters """
from openai import OpenAI
from dotenv import dotenv_values

class OpenRouterApi:
    """ Open Router Api """
    def __init__(self) -> None:
        dov = dotenv_values('models/.env')
        self.client = OpenAI(
                    base_url=dov["ENDPOINT"],
                    api_key=dov['APIKEY'],
                    )

    def get_answer(self, context: dict) -> str:
        """ Get answer """
        completion = self.client.chat.completions.create(
                                        model=context["model"],
                                        messages=context["messages"]
                                )
        return str(completion.choices[0].message.content)
