import json
import os

import seaborn

from 算各地60分鐘換算雨量 import RainCalculator


def paint_file(filename):
    with open(filename, 'r') as f:
        data = json.loads(f.readline())
        image = seaborn.heatmap(data)
        image.invert_yaxis()
        image.get_figure().savefig(filename+'.png')


if __name__ == "__main__":
    for root, dirnames, filenames in os.walk('60min_data'):
        paint_file('60min_data/'+filenames[0])
