import logging
import json

from flask import request, jsonify

from codeitsuisse import app
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor, DecisionTreeClassifier
import numpy as np

logger = logging.getLogger(__name__)

def todo(data):
    inp_arr = []
    for ele in (inp.split("\n")):
        # print(ele)
        if(len(ele) > 0):
            try:
                ele = ele.split(",")[3]
                inp_arr.append(float(ele))
            except:
                print(ele)

    import pandas as pd
    df = pd.DataFrame(
        {"close" : inp_arr}
    )
    df1 = pd.concat([df.shift(-4), df.shift(-3), df.shift(-2), df.shift(-1), df.shift(0)], axis=1 )
    df1.columns = ["y", "x1", "x2", "x3", "x4"]

    xtrain, xtest, ytrain, ytest = train_test_split(df1[["x1", "x2", "x3", "x4"]],df1['y'], test_size=0.2)
    model = DecisionTreeRegressor

    model = DecisionTreeRegressor()
    model.fit(
        xtrain, ytrain
    )

    model.score(
        xtest, ytest

    )

    p = model.predict(np.array(df1.iloc[258][1:5]).reshape(1,-1))
    return p[0]
    # print(inp_arr)


@app.route('/pre-tick', methods=['POST'])
def evaluatePT():
    data = request.get_data()
    logging.info("data sent for evaluation {}".format(data))
    
    result = todo(data)
    # logging.info("My result :{}".format(result))
    return json.dumps(result)
