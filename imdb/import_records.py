__author__ = 'Apurva A Kunkulol'

import os
import json
from pprint import pprint


def read_file():
    path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'imdb.json')
    #print(path)
    data = None
    with open(path, "r") as f:
        data = json.load(f)

    pprint("JSON data: {}\nType: {}".format(data[0], type(data)))




if __name__ == "__main__":
    read_file()
