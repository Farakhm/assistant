""" Mapper """
from models.adapters import OpenRouterApi
from models.decorators import worktime
from models.filer import Filer
from models.logger import loginit
logger1 = loginit(__name__, f"log/{__name__}.log")

class OpenRouterMapper:
    """ Open Router Mapper """
    def __init__(self, question: str, context: bool = True, save: bool = True) -> None:
        self.question = question
        self.completion = None
        self.context = context
        self.save = save

    @worktime
    def get_answer(
                    self,
                    model: str="deepseek/deepseek-chat-v3.1:free"
                    ) -> str:
        """ Answer """
        logger1.info("Request answer using %s", model)
        self.append_context_with_question()
        current_context = self.create_context(model)
        self.completion = OpenRouterApi().get_answer(current_context)
        self.append_context_with_answer()
        return self.completion

    def append_context_with_question(self) -> None:
        """ Append context with question """
        current_context = Filer('results/current_chat.json').loadDictFromJson()
        new_entry = {
                    "role": "user",
                    "content": f"{self.question}"
        }
        current_context.append(new_entry)
        Filer('results/current_chat.json').saveDictAsJson(current_context)

    def append_context_with_answer(self) -> None:
        """ Append context with answer """
        current_context = Filer('results/current_chat.json').loadDictFromJson()
        new_entry = {
                    "role": "assistant",
                    "content": f"{self.completion}"
        }
        current_context.append(new_entry)
        Filer('results/current_chat.json').saveDictAsJson(current_context)

    def create_context(self, model: str) -> dict:
        """ Context creating """
        current_sys = Filer('data/system.json').loadDictFromJson()
        current_context = Filer('results/current_chat.json').loadDictFromJson()
        result = [
                    {
                    "role": "system",
                    "content": f"{current_sys['general']}. User name is {current_sys['username']}, age is {current_sys['age']}"
                    }
                ]
        for c_c in current_context:
            result.append(c_c)
        return {
                "model": model,
                "messages": result
                }
