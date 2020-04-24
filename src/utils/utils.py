import os
import csv


def file_writer(direction, date, price):
    fields = locals()
    file_path = os.path.join(os.path.dirname(__file__), 'test.csv')
    if not os.path.isfile(file_path):
        with open(file_path, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fields.keys())
            writer.writeheader()
            writer.writerow(fields)
    else:
        with open(file_path, 'a') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(fields.values())
