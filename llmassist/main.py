""" Core """
from flask import Flask, request, render_template
from utils import clean_chat, save_used_model
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
            answer = OpenRouterMapper(
                                    request.form['question']
                                    ).get_answer(
                                        request.form['method']
                                        )
            return render_template(
                                    "index.html",
                                    answer = answer,
                                    models = models
                                    )
        elif 'exit' in request.form.keys():
            clean_chat(request.form['method'])
            return render_template(
                                    "goodbye.html"
                                    )
            
    return render_template("index.html",
                           models = models
                           )

def main():
    """ Main """
    app.run(debug=True)
