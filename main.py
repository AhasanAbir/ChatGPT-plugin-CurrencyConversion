import os
from waitress import serve
from flask import Flask, request, jsonify, send_from_directory
import requests

app = Flask(__name__)

# Get your API key from environment variables
my_secret = os.environ.get('ERD_API_KEY')

@app.route('/exchange_rate', methods=['GET'])
def exchange_rate():
    from_currency = request.args.get('from_currency')
    to_currency = request.args.get('to_currency')
    amount = float(request.args.get('amount'))
    date = request.args.get('date')

    try:
        converted_amount = get_exchange_rate(from_currency, to_currency, amount, date)
        response = {
            'from_currency': from_currency,
            'to_currency': to_currency,
            'amount': amount,
            'converted_amount': converted_amount
        }
        return jsonify(response), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

def get_exchange_rate(from_currency, to_currency, amount, date=None):
    url = "https://api.exchangeratesapi.io/convert"
    headers = {"apikey": my_secret}
    params = {
        "from": from_currency,
        "to": to_currency,
        "amount": amount
    }
    if date:
        params["date"] = date

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        result = response.json()
        return result["result"]
    else:
        raise Exception(f"Error: {response.status_code}, {response.text}")


@app.route('/.well-known/ai-plugin.json')
def serve_ai_plugin():
  return send_from_directory('.',
                             'ai-plugin.json',
                             mimetype='application/json')


@app.route('/.well-known/openapi.yaml')
def serve_openapi_yaml():
  return send_from_directory('.', 'openapi.yaml', mimetype='text/yaml')


if __name__ == '__main__':
    serve(app, host = "0.0.0.0", port = 8080)
