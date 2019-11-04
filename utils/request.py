import requests
import json
import logging


headers = {
  'content-type': 'application/json',
  'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'
}


def get(url, params=None, format=True):
    try:
        res = requests.get(url, params=params, headers=headers)
        if format:
            res = json.loads(res.text)
        return res
    except Exception as e:
        logging.error(e)
        return None
