from flask import Flask, request, jsonify
from common.scraper import parse

app = Flask(__name__)

@app.route("/api/quote", methods=['GET'])
def getQuote():
    ticker = request.args.get('ticker')
    onlyPrice = request.args.get('price')
    resp = parse(ticker)
    if onlyPrice != None:
        resp = resp['currentPrice']
    return jsonify(resp), 200

@app.route('/api/get_aplha_data/<string:symbol>/', methods=['GET'])
def get_alpha_data():
    return None

app.run(debug=True)
