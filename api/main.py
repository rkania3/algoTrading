from flask import Flask
import jsonify

app = Flask(__name__)


@app.route('/api/get_aplha_data/<string:symbol>/', methods=['GET'])
def get_alpha_data():
    return None


app.run(debug=True)