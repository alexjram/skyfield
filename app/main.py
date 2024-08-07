from flask import Flask, request
from skyfield_functions import get_constellations, get_stars_by_magnitude

app = Flask(__name__)

@app.route('/')
def hello():
    return '<h1>It works</h1>'

@app.route('/stars', methods=['GET'])
def get_stars() -> list:
    min_magnitude = request.args.get('min_magnitude', '-30')
    max_magnitude = request.args.get('max_magnitude', '1.5')
    
    return get_stars_by_magnitude(float(max_magnitude), float(min_magnitude))

@app.route('/constellations', methods=['GET'])
def get_constellations_route() -> list:
    return get_constellations()

app.run(host="0.0.0.0", debug=True, port=80)