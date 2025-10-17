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

def get_actual_models(
                    founded_models: list,
                    only_free: bool=True,
                    context: int = 50000,
                    time_diap: int = 15552000
                    ):
    """ Get actual and free models """
    ts_now = datetime.datetime.strptime(str(datetime.date.today()), "%Y-%m-%d").timestamp()
    if only_free:
        available_models = [x for x in founded_models 
                            if 'free' in x['id'] 
                            and (ts_now - x['created']) < time_diap
                            and x['context_length'] >= context]
    else:
        available_models = [x for x in founded_models 
                            if (ts_now - x['created']) < time_diap
                            and x['context_length'] >= context]
    Filer('data/available_models.json').saveDictAsJson(available_models)
    return [x['id'] for x in available_models]

def apply_founded_models() -> list:
    """ Apply """
    av_models = Filer('data/available_models.json').loadDictFromJson()
    models = [{"name": x['id'].split('/')[1],
               "choice": 0,
               "value": x['id']} for x in av_models]
    Filer('data/models.json').saveDictAsJson(models)
    return models
