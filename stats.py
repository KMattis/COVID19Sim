import argparse

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker


def read_stat_file(path):
    output = [], [], [], [], [], []
    with open(path, "r") as f:
        for line in f.readlines():
            record = [float(s) for s in line.split(",")[:-1]]
            for i in range(6):
                output[i].append(record[i])
    return output

def readBobbyFile(path):
    output = [], []
    with open(path, "r") as f:
        for line in f.readlines():
            record = line.split(",")[:-1]
            output[0].append(int(record[0]))
            output[1].append(record[1])
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

def readArgs():
    argparser = argparse.ArgumentParser(add_help=True)
    argparser.add_argument('-c', dest='category', help='the category to plot', type=str)
    args = argparser.parse_args()
    return args

def plotActivity():
    x,y1,y2,y3,y4,y5 = read_stat_file("logfiles/activity.log")
    
    x = (1/60) * np.array(x)
    
    plt.plot(x, np.array(y1), label = "Travelling")
    plt.plot(x, np.array(y4), label = "Sleep")
    plt.plot(x, np.array(y3), label = "Outdoor")
    plt.plot(x, np.array(y5), label = "Work")
    plt.plot(x, np.array(y2), label = "Eat")
    
    plt.legend(loc='upper center', shadow=True, fontsize='x-large')
    
    plt.grid(True)
    plt.xticks(np.arange(0, np.max(x), 6))
    plt.show() 
    
def plotBobby():
    time, activity = readBobbyFile("logfiles/bobby.log")
    
    eat = sum(1 for a in activity if a == "EAT")
    sleep = sum(1 for a in activity if a == "SLEEP")
    work = sum(1 for a in activity if a == "WORK")
    outdoor = sum(1 for a in activity if a == "OUTDOOR")

    time = (1/60) * np.array(time)

    # plt.pie(np.array([eat, sleep, work, outdoor]), labels = [ "Eat", "Sleep", "Work", "Outdoor" ])
    
    color = { "EAT": "#8800FF", "SLEEP": "#FF8800", "WORK": "#FF0000", "OUTDOOR": "#008800" }
    colors = [color[a] for a in activity]
    heights = np.ones(len(time))
    plt.bar(time, height=1, width=5, color=colors)

    plt.grid(True)
    plt.xticks(np.arange(0, np.max(time), 6))
    plt.show()

    

if __name__ == "__main__":
    args = readArgs()

    if args.category == "activity":
        plotActivity()
    elif args.category == "bobby":
        plotBobby()
