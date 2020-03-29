import argparse

import numpy as np
import matplotlib.pyplot as plt


def read_stat_file(path):
    output = [], [], [], [], [], []
    with open(path, "r") as f:
        for line in f.readlines():
            record = [float(s) for s in line.split(",")[:-1]]
            for i in range(6):
                output[i].append(record[i])
    return output

def moving_average(a, n=5):
    l = len(a)
    output = []

    for i in range(l):
        min_idx = max(0, i-n)
        max_idx = min(l, i+n+1)

        output.append(0)
        for j in range(min_idx, max_idx):
            output[-1] += a[j]

        output[-1] /= max_idx - min_idx
    
    return output

def read_args():
    argparser = argparse.ArgumentParser(add_help=True)
    argparser.add_argument('-c', dest='category', help='the category to plot', type=str)
    args = argparser.parse_args()
    return args

if __name__ == "__main__":
    args = read_args()

    x,y1,y2,y3,y4,y5 = read_stat_file("logfiles/" + args.category + ".log")

    x = (1/60) * np.array(x)

    plt.plot(x, np.array(y1), label = "Travelling")
    plt.plot(x, np.array(y2), label = "Home")
    plt.plot(x, np.array(y3), label = "Service")
    plt.plot(x, np.array(y4), label = "Nonservice")
    plt.plot(x, np.array(y5), label = "Outdoor")

    plt.legend(loc='upper center', shadow=True, fontsize='x-large')

    plt.grid(True)
    plt.show() 

