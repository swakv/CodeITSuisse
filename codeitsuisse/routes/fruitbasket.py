import logging
import json

from flask import request, jsonify
from codeitsuisse.routes.fruit import EXPORT
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
    result = 0
    # {'maRamubutan': 17, 'maPineapple': 23, 'maApple': 75} our result 2880 10 20 30
    # {'maPomegranate': 29, 'maRamubutan': 58, 'maApple': 76} our result 6770 10 20 70 
    for key, val in data.items():
        if key in EXPORT:
            result += EXPORT[key]*val
        else:
            logging.info("New Fruit {}".format(key))
            result += val*50
            
    logging.info("data sent for evaluation {}".format(data))
    logging.info("My result :{}".format(result))
    return json.dumps(result)
