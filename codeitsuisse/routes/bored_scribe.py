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
    for i in range(len(s)):
        for j in range(i+2, len(s)+1):
            temp = s[i:j]
            if temp == temp[::-1]:
                if j-i > max_val:
                    max_val = j-i
                    max_palindrome = temp
                counter += 1
    return counter, max_palindrome


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
        n = 0
        word_len_counter = 2
        word_list = wordninja.split(attempt)
        attempts_list.append(word_list)

    start_string = min(attempts_list, key=len)
    cur_string = "".join(start_string)
    count, max_string = countPallindrome(cur_string)
    counter = 0
    while True:
        ceaser_key = sum(list(map(lambda x: ord(x), max_string)))+count
        new_str = encrypt(cur_string, ceaser_key)
        counter += 1
        # print(new_str, input_str)
        if new_str == input_str:
            break
        cur_string = new_str
        count, max_string = countPallindrome(cur_string)

    return {"id": id_in, "encryptionCount": counter, "originalText":  " ".join(start_string)}

@app.route('/bored-scribe', methods=['POST'])
def evaluateBS():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    answer = []
    for case in data:
        answer.append(scribe(case['encryptedText'],case['id']))
    result = answer
    logging.info("My result :{}".format(result))
    return json.dumps(result)
