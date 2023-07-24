import os.path
from flask import Flask, request
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
    except (KeyError, ValueError, TypeError):
        return 'Invalid calculation', 400

    result = calculate_return(p, InterestRate(i), Contribution(c, f), d)
    return '{}'.format(result)


if __name__ == '__main__':
    serve(app, host='0.0.0.0', port='8000')
