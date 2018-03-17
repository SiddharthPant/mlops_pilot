
"""
API to generate word counts and get word count
"""

import json
import os
from bottle import route, run, request
from collections import Counter, OrderedDict
import re
import logging
from datetime import datetime

# Logging config
logger = logging.getLogger('root')
FORMAT = "[%(asctime)s] - %(funcName)20s() - %(message)s"
logfile = 'logs/wordcount_{0}.log'.format(datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
logging.basicConfig(filename=logfile,
                    level=logging.DEBUG, format=FORMAT)

file_path = 'big.txt'
stop_words = open('stopwords.txt').read()
punctuations = [',', '!', ':', '?', '_']


def preprocess(path):
    """
    Preprocesses the data by removing stop words and returns word counts
    """
    logger.info('Pre-Processing started.')
    words = re.findall(r'\w+', open(path).read().lower())
    filtered_words = [w for w in words if (
        w not in stop_words and w not in punctuations)]
    count = Counter(filtered_words)
    response = OrderedDict(count.most_common())
    
    logger.info('Pre-Processing completed.')
    
    return response


word_counts = preprocess(file_path)


@route('/words/')
def list_word_counts():
    """
    Returns the word counts of all words present in a given file
    """
    response = {
        "success": True,
        "info": word_counts
    }

    logger.info("response: " + str(response))
    return response


@route('/words/top/<n:int>', method='GET')
def list_top_word(n):
    """
    Returns the top words in a given file based on their frequency
    """

    if (n > len(word_counts)):
        response = {"success": True, "info": "Input no is Out of range of dictionary length:"}
    else:
        response = {"success": True, "info": dict((word_counts.items())[:n])}

    logger.info("response: " + str(response))
    
    return response


@route('/words/counts/<word>', method='GET')
def get_word_count(word):
    """
    Returns the word count of a word if it is present
    """
    try:
        response = {"success": True, "count": word_counts[word]}
    except KeyError:
        response = {"success": False, "info": "Word not present"}
    
    logger.info("response: " + str(response))
    
    return response


@route('/words/add', method='PUT')
def add_word():
    """
    Updates the word count of the words passed
    """

    data = json.loads(request.body.read())
    word_counts.update(data)

    response = {"success": True, "info": "Words %s added in the dictionary!" % data.keys()}

    logger.info("response: " + str(response))
    
    return response


@route('/words/remove/<word>', method='DELETE')
def remove_word(word):
    """
    Removes the word from the word count dictionary if it is present
    """
    try:
        del word_counts[word]
        response = {"success": True, "info": "Word %s removed from the dictionary!" % word}
    except KeyError:
        response = {"success": False, "info": "Word not present in the dictionary!"}
        
    logger.info("response: " + str(response))
    
    return response


if __name__ == '__main__':
    run(host='0.0.0.0', port=8080, debug=True)
