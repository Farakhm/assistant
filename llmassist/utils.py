""" Utils """
import datetime
from random import randint
from models.filer import Filer

def clean_chat(model: str) -> None:
    """ Cleaning chat file """
    result = {}
    result['model'] = model
    result['date'] = datetime.datetime.now().timestamp()
    result['chat'] = Filer('results/current_chat.json').loadDictFromJson()
    Filer(f'archives/chat_{randint(10000, 99999)}.json').saveDictAsJson(result)
    Filer('results/current_chat.json').deleteFile()
    Filer('results/current_chat.json').saveDictAsJson([])

def save_used_model(used_model: str) -> list:
    """ Saving used models """
    models = Filer('data/models.json').loadDictFromJson()
    for model in models:
        if model['value'] == used_model:
            model['choice'] = 1
        else:
            model['choice'] = 0
    Filer('data/models.json').saveDictAsJson(models)
    return models
