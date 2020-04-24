import argparse
from macd import build_macd_histogram
from datetime import datetime
from utils.point import Point
from utils.utils import file_writer
from utils.rules import first_rule_open, first_rule_close, second_rule_open, second_rule_close
from test import data_appl_60, data_appl_30
from services.finnhub_service import get_client


def enter_market(frame_fragment):
    file_writer(frame_fragment[1].date, 'BUY', frame_fragment[1].open)
    return True


def exit_market(frame_fragment):
    file_writer(frame_fragment[1].date, 'SELL', frame_fragment[1].open)
    return False


def data_frame_open_processing(histogram, data_frame, counter):
    first_point = None
    second_point = None
    points = []
    for i, df in zip(range(counter-2, 0, -1), data_frame.iterrows()):
        if histogram[i-1] < histogram[i] > histogram[i+1]:
            points.append(Point(histogram[i], df))

    for i in range(len(points)-1):
        for z in range(i+1, len(points)):
            if points[i].histogram >= points[z].histogram:
                if first_rule_open(points[i], points[z]) or second_rule_open(points[i], points[z]):
                    first_point = points[i].histogram
                    second_point = points[z].histogram
                    break
        else:
            continue
        break
    return first_point, second_point


def data_frame_close_processing(histogram, data_frame, counter):
    first_point = None
    second_point = None
    points = []
    for i, df in zip(range(counter-2, 0, -1), data_frame.iterrows()):
        if (histogram[i-1] > histogram[i] < histogram[i+1]) and histogram[i-1] < 0 and histogram[i] < 0 and histogram[i+1] < 0:
            points.append(Point(histogram[i], df))

    if len(points) < 2:
        return None, None
    else:
        for i in range(len(points)-1):
            for z in range(i+1, len(points)):
                if points[i].histogram <= points[z].histogram:
                    if first_rule_close(points[i], points[z]) or second_rule_close(points[i], points[z]):
                        first_point = points[i]
                        second_point = points[z]
                        break
            else:
                continue
            break
    return first_point, second_point


def start_monitoring(*args):
    # response_60 = get_client('AAPL', resolution=60, start='2018-01-01 00:00:00')
    # response_30 = get_client('AAPL', resolution=30, start='2018-01-01 00:00:00')
    response_60 = data_appl_60
    response_30 = data_appl_30
    is_opened = False
    first = None
    second = None
    histogram, _, data_frame = build_macd_histogram(response_60)
    his = 0
    for his, df in zip(histogram, data_frame.iterrows()):
        print(his)
        print(f'len: {len(histogram)}')
        if first and second and not is_opened:
            is_opened = enter_market(df)
            first = None
            second = None
            histogram, _, data_frame = build_macd_histogram(response_30, df[1].date)
            his = 0
        if first and second and is_opened:
            is_opened = exit_market(df)
            first = None
            second = None
            histogram, _, data_frame = build_macd_histogram(response_60, df[1].date)
            his = 0
        try:
            if not is_opened and histogram[his] < 0:
                first, second = data_frame_open_processing(histogram, data_frame, his)
            if is_opened and histogram[his] > 0:
                first, second = data_frame_close_processing(histogram, data_frame, his)
        except KeyError:
            print(len(histogram))
            print(his)
            break


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', help='Stock ticker.')
    args = parser.parse_args()
    start_monitoring(args.t)
