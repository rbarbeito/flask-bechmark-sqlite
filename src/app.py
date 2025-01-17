from flask import Flask, request, render_template, jsonify, make_response

from functions import my_functions as mf
from functions.db import MyDataBase

db = MyDataBase()


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/bechmark', methods=['POST'])
def bechmark():
    data = request.get_json()

    bechmark = mf.bechmark_action(servidor=data['servicio'],
                                  endpoint=data['url'],
                                  n=data['request'],
                                  c=data['concurrency'],)

    if bechmark["code"] != 'success':
        return make_response(jsonify(bechmark), 500)

    return make_response(jsonify(bechmark), 201)


@app.route('/graphics')
def graphics():
    return render_template('graphics.html')


@app.route('/data')
def getData():

    data = db.get_consultas()
    resp = {}
    for i in data:
        if i['server'] not in resp.keys():
            resp[i['server']] = [i['id']]
        else:
            resp[i['server']].append(i['id'])

    return make_response(jsonify(resp), 200)


@app.route('/general')
def general():
    data = db.get_general()

    stadisticas = {}

    services = ''

    # for i in range(len(data)):
    #   	data[i]['software']

    #     for key, value in data[i]:
    #         if data[i]['software']==services:

    return data


if __name__ == '__main__':

    app.run(debug=True)
