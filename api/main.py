from flask import Flask, request, jsonify
from common.scraper import parse

app = Flask(__name__)

@app.route("/quote")
def getQuote():
    ticker = request.args.get('ticker')
    onlyPrice = request.args.get('price')
    resp = parse(ticker)
    if onlyPrice != None:
        resp = resp['currentPrice']
    return jsonify(resp), 200

if __name__ == '__main__':
   app.run(host='0.0.0.0', port=8000, threaded=True)