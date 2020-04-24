import argparse
from macd import build_macd_histogram
from utils.point import Point
from utils.utils import file_writer
from utils.rules import first_rule_open, first_rule_close, second_rule_open, second_rule_close
from test_data import data_appl_60


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
    response_60 = data_appl_60
    is_opened = False
    first = None
    second = None
    histogram, _, data_frame = build_macd_histogram(response_60)
    for his, df in zip(range(len(histogram)-1), data_frame.iterrows()):
        if first and second and not is_opened:
            is_opened = enter_market(df)
            first = None
            second = None
        if first and second and is_opened:
            is_opened = exit_market(df)
            first = None
            second = None
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
