import logging
import json

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)


@app.route('/contact_trace', methods=['POST'])
def evaluateCT():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    # inputValue = data.get("input")
    # logging.info("Input Data: {}".format(inputValue))
    # result = inputValue * inputValue
    # logging.info("My result :{}".format(result))
    # return json.dumps(result)
