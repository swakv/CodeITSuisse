import logging
import json
import numpy as np

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)


@app.route('/salad-spree', methods=['POST'])
def evaluateSP():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    n = data.get("number_of_salads")
    arr = data.get("salad_prices_street_map")

    arr_int = arr

    for i in range(len(arr)):
        for j in range(len(arr[i])):
            if arr[i][j] == "X":
                arr_int[i][j] = np.inf
            else:
                arr_int[i][j] = int(arr[i][j])

    arr_sum = []

    # arr = np.array([10, 20, 30, 40, 50])
    for i in range(len(arr_int)):
        sums  = np.convolve(arr_int[i], np.ones(n, dtype=np.int), mode='valid')
        arr_sum+=list(sums)

    arr_sum = np.array(arr_sum)
    min_val = arr_sum.min()
    if min_val == np.inf:
        ans = 0
    else:
        ans = min_val

    result = int(ans)
    logging.info("My result :{}".format(result))
    return json.dumps(result)
