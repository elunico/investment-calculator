import os.path
from flask import Flask, request, jsonify
from waitress import serve
from main import calculate_return, InterestRate, Contribution, TimeUnit, DollarAmount, MONTH, DAY, WEEK, YEAR
app = Flask(__name__)


def frequency_for(formdata):
    match formdata:
        case 'weekly': return WEEK
        case 'daily': return DAY
        case 'monthly': return MONTH
        case 'yearly': return YEAR

    raise ValueError("Unknown frequency value {}".format(formdata))


@app.get('/')
def index():
    with open(os.path.join('static', 'index.html')) as f:
        return f.read()


@app.post('/calculate')
def calculate():
    b = request.json
    try:
        p = float(b['principle'])
        i = float(b['interest']) / 100
        c = float(b['contribution'])
        f = frequency_for(b['frequency'])
        d = int(b['duration'])
        result = calculate_return(p, InterestRate(i), Contribution(c, f), d)
    except (KeyError, ValueError, TypeError) as e:
        return jsonify({'message': 'Interest calculation parameters are invalid'}), 400

    return jsonify({'principle': result.starting, 'interest': result.interest, 'contributions': result.contributed, 'total': result.total})


if __name__ == '__main__':
    serve(app, host='0.0.0.0', port='8000')
