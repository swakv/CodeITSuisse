import logging
import json

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)


@app.route('/salad-spree', methods=['POST'])
def evaluateSP():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    result = {}
    return json.dumps(result)
