import logging
import json

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)


def line_intersection(line1, line2):
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
       return 0

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div


    if isBetween(line2[0], line2[1], (x,y)): 
        return round(x, 2), round(y, 2)
    else:
        return 0

def isBetween(a, b, c):
    if a == c or b ==c:
        return False

    crossproduct = (c[1] - a[1]) * (b[0] - a[0]) - (c[0] - a[0]) * (b[1] - a[1])

    # compare versus epsilon for floating point values, or != 0 if using integers
    if abs(crossproduct) > 0.00000001:
        return False

    dotproduct = (c[0] - a[0]) * (b[0] - a[0]) + (c[1] - a[1])*(b[1] - a[1])
    if dotproduct < 0:
        return False

    squaredlengthba = (b[0] - a[0])*(b[0] - a[0]) + (b[1] - a[1])*(b[1] - a[1])
    if dotproduct > squaredlengthba:
        return False

    return True




@app.route('/revisitgeometry', methods=['POST'])
def evaluateRG():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    arr = []
    shape_arr = []
    line_arr = []
    final_arr = []

    for val in data["shapeCoordinates"]:
        arr = val["x"], val["y"]
        shape_arr.append(arr)

    for val in data["lineCoordinates"]:
        arr = val["x"], val["y"]
        line_arr.append(arr)

    # print(line_arr, shape_arr)
    line1 = (line_arr[0], line_arr[1])

    for j in range(len(shape_arr)):
        if j == len(shape_arr) - 1:
            line2 = (shape_arr[j], shape_arr[0])
        else:
            line2 = (shape_arr[j], shape_arr[j+1])
        ans = line_intersection(line1, line2)
        if ans != 0:
            final_arr.append(ans)

    result = [{"x": val[0],"y":val[1]} for val in final_arr]
    logging.info("My result :{}".format(result))
    return json.dumps(result)
