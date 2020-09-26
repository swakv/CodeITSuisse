import logging
import json

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)

import operator as op
from functools import reduce

def ncr(n, r):
    r = min(r, n-r)
    numer = reduce(op.mul, range(n, n-r, -1), 1)
    denom = reduce(op.mul, range(1, r+1), 1)
    return numer // denom

def distancing(seats = 8, people = 3,spaces = 1):
    possible_spaces = seats-(people*spaces)
    to_choose = people
    result = 0
    if to_choose<=possible_spaces:
        result+=ncr(possible_spaces, to_choose)
    for x in range(1,spaces+1):
        cur_people = people-1
        cur_seats = seats-x
        possible_spaces = cur_seats - (cur_people*spaces)
        to_choose = cur_people
        if to_choose<=possible_spaces:
            result+=ncr(possible_spaces, to_choose)
    return result

@app.route('/social_distancing', methods=['POST'])
def evaluateSD():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    answer = {}
    for key, val in data['tests'].items():
        answer[key] = distancing(**val)

    result = {"answers":answer}
    logging.info("My result :{}".format(result))
    return json.dumps(result)
