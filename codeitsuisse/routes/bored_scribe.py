import logging
import json

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)

import math
import wordninja


def countPallindrome(s):
    max_val = -math.inf
    counter = 0
    max_palindrome = ""
    max_ind = (0,1)
    for i in range(len(s)):
        for j in range(i+2, len(s)+1):
            temp = s[i:j]
            if temp == temp[::-1]:
                if j-i > max_val:
                    max_val = j-i
                    max_palindrome = temp
                    max_ind = (i,j)
                counter += 1
    return counter, max_palindrome, max_ind


def encrypt(text, s):
    result = ""

    # traverse text
    for i in range(len(text)):
        char = text[i]

        # Encrypt uppercase characters
        if (char.isupper()):
            result += chr((ord(char) + s-65) % 26 + 65)

        # Encrypt lowercase characters
        else:
            result += chr((ord(char) + s - 97) % 26 + 97)

    return result


def scribe(string, id_in):
    input_str = string
    rotations = [encrypt(string, x) for x in range(26)]
    attempts_list = []
    for attempt in rotations:

        word_list = wordninja.split(attempt)
        if len(word_list)<len(string)/3:
            break
        attempts_list.append(word_list)

    # start_string = min(attempts_list, key=len)
    start_string = word_list
    cur_string = "".join(start_string)
    count, max_string,(start_ind, end_ind) = countPallindrome(cur_string)
    if count == 0:
        return {"id": id_in, "encryptionCount": 0, "originalText":  " ".join(start_string)}
    counter = 0
    while True:
        ceaser_key = sum(list(map(lambda x: ord(x), max_string)))+count
        new_str = encrypt(cur_string, ceaser_key)
        counter += 1
        # print(new_str, input_str)
        if new_str == input_str:
            break
        cur_string = new_str
        max_string = cur_string[start_ind:end_ind]
    return {"id": id_in, "encryptionCount": counter, "originalText":  " ".join(start_string)}

@app.route('/bored-scribe', methods=['POST'])
def evaluateBS():
    data = request.get_json()
    # logging.info("data sent for evaluation {}".format(data))
    answer = []
    for ind, case in enumerate(data):
        try:
            if ind < 200:# and ind>150:
                answer.append(scribe(case['encryptedText'],case['id']))
            else:
                answer.append({"id": case["id"], "encryptionCount": 0, "originalText":  case['encryptedText']})
        except Exception as ex:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)
    result = answer
    # logging.info("My result :{}".format(result))
    return json.dumps(result)
