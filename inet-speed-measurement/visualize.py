import argparse
import csv
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os

from datetime import datetime
from matplotlib import style


def read_params():
    parser = argparse.ArgumentParser(description='speedtest results visualizer')
    parser.add_argument(dest='file_name', type=str, help='input file')
    return parser.parse_args()


def moving_average(a, n):
    length = len(a)
    return np.array([np.mean(a[i:i + n]) for i in np.arange(0, length - n + 1)])


AVERAGE_WINDOW = 15


def main(args):
    style.use('ggplot')

    time = []
    speed = []
    with open(args.file_name, "r") as in_file:
        input_data = csv.reader(in_file, delimiter=',', quotechar='"')
        for row in input_data:
            if len(row) == 12:
                idx = 6
            elif len(row) == 13:
                idx = 7
            else:
                print(row)
                continue
            time.append(datetime.strptime(row[0], '%Y-%m-%dT%H:%M:%S'))
            speed.append(float(row[idx]) * 8.0 / 1e6)

    avr_time = [datetime.fromtimestamp(t) for t in moving_average([t.timestamp() for t in time], AVERAGE_WINDOW)]
    avr_speed = moving_average(speed, AVERAGE_WINDOW)

    fig, ax = plt.subplots()
    ax.plot(time, speed)
    ax.plot(avr_time, avr_speed, linewidth=4)
    max_speed = max(speed)
    ax.set_ylim(0, max_speed * 1.1)

    plt.title(f'Connection Speed ({os.path.split(args.file_name)[1]})')
    plt.xlabel('Time')
    plt.ylabel('Speed')
    xfmt = mdates.DateFormatter('%Y-%m-%d %H:%M:%S')
    ax.xaxis.set_major_formatter(xfmt)

    fig.autofmt_xdate()
    plt.show()


if __name__ == "__main__":
    args = read_params()
    main(args)