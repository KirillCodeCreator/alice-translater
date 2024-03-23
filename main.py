import logging
import os

import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

logging.basicConfig(level=logging.INFO, filename='app.log',
                    format='%(asctime)s %(levelname)s %(name)s %(message)s')

translator_url = 'https://translate.yandex.net/api/v1.5/tr.json/translate'
translator_api_key = 'trnsl.1.1.20190414T112602Z.28565479fb179187.ee436856ac2d0c7e02e4a62e755a4fffa15baa95'


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
        res['response']['text'] = translate(word)


def translate(word):
    params = {
        'key': translator_api_key,
        'text': word,
        'lang': 'ru-en'
    }
    data = requests.get(translator_url, params).json()

    if data["code"] == 200:
        return data['text'][0]
    elif data["code"] == 401:
        return 'Неправильный API-ключ'
    elif data["code"] == 402:
        return 'API-ключ заблокирован'
    elif data["code"] == 404:
        return 'Превышено суточное ограничение на объем переведенного текста'
    elif data["code"] == 413:
        return 'Превышен максимально допустимый размер текста'
    elif data["code"] == 422:
        return 'Текст не может быть переведен'
    elif data["code"] == 501:
        return 'Заданное направление перевода не поддерживается'
    else:
        return f'Получен код ответа {data["code"]}'


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
