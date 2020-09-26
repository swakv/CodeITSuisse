import logging
import json

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)


@app.route('/fruitbasket', methods=['POST'])
def evaluateMFB():
    data = request.get_json()
    if data == None:
        return 0
    logging.info("data sent for evaluation {}".format(data))
    a = data['maApple']
    w = data['maWatermelon']
    b = data['maBanana']
    ans = a*10 + w*20 + b*30 
    result = ans
    logging.info("My result :{}".format(result))
    return json.dumps(result)
