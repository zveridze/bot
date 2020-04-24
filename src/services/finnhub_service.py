from datetime import datetime
import settings
import requests
from requests.exceptions import ConnectionError
from json.decoder import JSONDecodeError


def get_client(ticker=None, resolution=60, start=None, end='2020-12-31 23:59:59'):
    if not settings.API_KEY:
        raise ValueError('Api-key for "Finnhub" does not set up. Please set up api-key.')
    if not ticker:
        raise ValueError('Ticker does not define! Please set up ticker.')
    params = {
        'symbol': ticker,
        'resolution': resolution,
        'from': datetime.timestamp(datetime.strptime(start, '%Y-%m-%d %H:%M:%S')) if start else '1514764800',
        'to': datetime.timestamp(datetime.strptime(end, '%Y-%m-%d %H:%M:%S')) if end else datetime.timestamp(datetime.now()),
        'token': settings.API_KEY
    }

    try:
        r = requests.get(
            url=settings.FINNHUB_API_URL,
            params=params
        )
        if r.json()['s'] == 'no_data':
            raise ValueError('No data for this ticker. Please choose another one.')
        return r.json()
    except JSONDecodeError:
        print('Something went wrong. Please try again later.')
        return None
    except ConnectionError:
        print('Service unavailable. Please try again later.')
        return None
