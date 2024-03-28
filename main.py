import logging
import os

from flask import Flask, request, jsonify
from translate import Translator

app = Flask(__name__)

logging.basicConfig(level=logging.INFO, filename='app.log',
                    format='%(asctime)s %(levelname)s %(name)s %(message)s')


@app.route('/post', methods=['POST'])
def main():
    logging.info('Request: %r', request.json)
    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }
    handle_dialog(response, request.json)
    logging.info('Response: %r', response)
    return jsonify(response)


def handle_dialog(res, req):
    if req['session']['new']:
        res['response']['text'] = 'Привет! Я могу переводить слова! Пример: Переведи слово стакан'
    else:
        word = req['request']['nlu']['tokens'][-1]
        res['response']['text'] = translate_translator(word)


translator = Translator(from_lang="ru", to_lang="en")


def translate_translator(word):
    global translator
    translation = translator.translate(word)
    return translation


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
