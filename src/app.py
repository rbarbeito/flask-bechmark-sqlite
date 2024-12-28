from flask import Flask, request, render_template, jsonify, make_response

from functions import my_functions as mf


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


if __name__ == '__main__':

    app.run(debug=True)
