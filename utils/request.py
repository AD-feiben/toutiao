import requests
import json
import logging


headers = {
  'content-type': 'application/json',
  'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'
}


def get(url, params):
    try:
        r = requests.get(url, params=params, headers=headers)
        res = json.loads(r.text)
        return res
    except Exception as e:
        logging.error(e)
        return None
