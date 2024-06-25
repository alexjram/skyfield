from flask import Flask, request
from skyfield_functions import get_stars_by_magnitude

app = Flask(__name__)

@app.route('/')
def hello():
    return '<h1>It works</h1>'

@app.route('/stars', methods=['GET'])
def get_stars() -> list:
    min_magnitude = request.args['min_magnitude']
    max_magnitude = request.args['max_magnitude']
    
    return get_stars_by_magnitude(float(max_magnitude), float(min_magnitude))


app.run(host="0.0.0.0", debug=True, port=80)