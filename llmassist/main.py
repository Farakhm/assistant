""" Core """
from flask import Flask, request, render_template
from utils import clean_chat, save_used_model, get_actual_models, apply_founded_models
from models.mapper import OpenRouterMapper
from models.filer import Filer

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
@app.route('/index', methods=['POST', 'GET'])
def index():
    """ Main window """
    models = Filer('data/models.json').loadDictFromJson()
    if request.method == 'POST':
        if "ask" in request.form.keys():
            models = save_used_model(request.form['method'])
            try:
                answer = OpenRouterMapper(
                                        request.form['question']
                                        ).get_answer(
                                            request.form['method']
                                            )
            except Exception as ex:
                answer = f"Ошибка запроса: {ex}"
            return render_template(
                                    "index.html",
                                    answer = answer,
                                    models = models
                                    )
        elif 'tune' in request.form.keys():
            return render_template('tune.html',
                                    models=models,
                                    only_free = True,
                                    context = 50000,
                                    days = 180
                                   )
        elif 'exit' in request.form.keys():
            clean_chat(request.form['method'])
            return render_template(
                                    "goodbye.html"
                                    )
    return render_template("index.html",
                           models = models
                           )

@app.route('/tune', methods=['POST', 'GET'])
def tune():
    """ Tune window """
    models = Filer('data/available_models.json').loadDictFromJson()
    if request.method == 'POST':
        if 'free' in request.form.keys():
            only_free = True
        else:
            only_free = False
        context = int(dict(request.form)['context'])
        days = int(dict(request.form)['days'])
        if 'lst' in request.form.keys():
            answer = get_actual_models(
                OpenRouterMapper().get_models_list(),
                only_free,
                context,
                days*3600*24
                )
            return render_template(
                                    "tune.html",
                                    answer = '\n'.join(answer),
                                    models = models,
                                    only_free = only_free,
                                    context = context,
                                    days = days
                                    )
        elif 'apply' in request.form.keys():
            models = apply_founded_models()
            return render_template(
                                    "tune.html",
                                    answer = "",
                                    models = models,
                                    only_free = only_free,
                                    context = context,
                                    days = days
                                    )
        elif 'exit' in request.form.keys():
            models = Filer('data/models.json').loadDictFromJson()
            return render_template("index.html",
                                    models = models
                                    )
    return render_template("index.html",
                           models = models
                           )

def main():
    """ Main """
    app.run(debug=True)
