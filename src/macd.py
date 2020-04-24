import pandas as pd
from datetime import datetime
from test import data_appl_60, data_appl_30


def build_macd_histogram(response, date=None):
    counter = 0
    if date:
        for i in range(len(response['t'])):
            if response['t'][i] == date.timestamp():
                counter = i
    data_frame = pd.DataFrame({'date': [datetime.utcfromtimestamp(date) for date in response['t'][counter:]],
                               'low': response['l'][counter:], 'high': response['h'][counter:],
                               'open': response['o'][counter:], 'close': response['c'][counter:]})
    exp_fast = data_frame.close.ewm(span=12, adjust=False).mean()
    exp_slow = data_frame.close.ewm(span=26, adjust=False).mean()
    histogram = exp_fast - exp_slow
    signal_line = histogram.ewm(span=9, adjust=False).mean()
    return histogram, signal_line, data_frame


# date = datetime.strptime('2019-11-15 15:00:00', '%Y-%m-%d %H:%M:%S')
# _,_,df =build_macd_histogram(data_appl_60, date)
# for i in df.iterrows():
#     print(i[1].date)