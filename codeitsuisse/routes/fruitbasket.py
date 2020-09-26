import logging
import json

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)


@app.route('/fruitbasket', methods=['POST'])
def evaluateMFB():
    data = request.get_data()
    encoding = 'utf-8'
    data = data.decode(encoding)
    print(data)
    data = eval(data)
    arr = []
    for key, val in data.items():
        arr.append(val)
    
    logging.info("data sent for evaluation {}".format(data))
    result = arr[0]*10 + arr[1]*20 + arr[2]*30
    logging.info("My result :{}".format(result))
    return json.dumps(result)
