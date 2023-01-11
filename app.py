import logging

from scraper import Scraper
from flask import Flask, request, jsonify

logging.basicConfig(
    level=logging.INFO, 
    format="%(asctime)s | %(levelname)s | %(message)s", 
    handlers=[logging.StreamHandler()])

scraper = Scraper(delay = 1)
app     = Flask(__name__)



@app.route('/barcode/find')
def get_data_from_barcode():
    barcode = request.args.get('barcode')
    data = scraper.run(barcode)
    return jsonify(data)



if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 5000)
