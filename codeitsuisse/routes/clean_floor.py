import logging
import json

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)


@app.route('/clean_floor', methods=['POST'])
def evaluateCF():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    answers = {}
    for test_id, val in data['tests'].items():
        floor = val["floor"][::-1]
        count = 0
        while floor:
            if len(floor)==1:
                if floor[-1]%2 == 0:
                    count+= (2* floor[-1])
                else:
                    count+= (2* floor[-1]) +1
                
                break
            count+= floor[-1]*2+1
            if floor[-1]>=floor[-2]:
                if (floor[-1]-floor[-2])%2==0:
                    if len(floor) != 2:
                        floor[-2] = 1
                        floor.pop()
                    else:
                        floor.pop()
                        floor.pop()
                        count -= 1
                        break
                else:
                    floor.pop()
                    floor.pop()
                    try:
                        floor[-1] -= 1
                        count+=1
                    except:
                        break
            else:
                floor[-2]-=floor[-1]
                floor[-2]-=1
                floor.pop()
        answers[test_id] = count

    result = {"answers":answers}
    logging.info("My result :{}".format(result))
    return json.dumps(result)
