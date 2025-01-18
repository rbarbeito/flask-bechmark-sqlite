from flask import Flask, request, render_template, jsonify, make_response, redirect, url_for
import requests

from functions import my_functions as mf
from functions.db import MyDataBase

from collections import defaultdict

db = MyDataBase()


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('graphics.html')


@app.route('/graphics')
def graphics():
    return redirect(url_for('index'), 308)



@app.route('/bechmark', methods=['GET', 'POST'])
def bechmark():

    if requests.methods == 'GET':
        return render_template('index.html')
    else:
        data = request.get_json()
        bechmark = mf.bechmark_action(servidor=data['servicio'],
                                      endpoint=data['url'],
                                      n=data['request'],
                                      c=data['concurrency'],)

        if bechmark["code"] != 'success':
            return make_response(jsonify(bechmark), 500)

        return make_response(jsonify(bechmark), 201)


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

    sums = defaultdict(lambda: defaultdict(float))
    counters = defaultdict(lambda: defaultdict(int))

    for entry in data:
        software = entry['software']
        for key, value in entry.items():
            if isinstance(value, (int, float)) and key != 'id':
                sums[software][key] += value
                counters[software][key] += 1

    averages = {
        software: {key: sums[software][key] /
                   counters[software][key] for key in sums[software]}
        for software in sums
    }

    return averages


@app.route('/generalbyservices/<servidor>')
def generalbyservices(servidor):
    data = db.get_generalbyservices(servidor)
    return make_response(jsonify(data), 200)


if __name__ == '__main__':

    app.run(debug=True)
