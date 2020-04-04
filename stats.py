import argparse

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker


def read_stat_file(path, num):
    output = [[] for _ in range(num)]
    with open(path, "r") as f:
        for line in f.readlines():
            record = [float(s) for s in line.split(",")[:-1]]
            for i in range(num):
                r = record[i]
                output[i].append(r)
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

def plotActivity(path):
    data = read_stat_file(path, 7)
    x = data[0]
    
    x = (1/60) * np.array(x)
    
    plt.plot(x, np.array(data[1]), label = "Travelling")
    plt.plot(x, np.array(data[4]), label = "Sleep")
    plt.plot(x, np.array(data[3]), label = "Outdoor")
    plt.plot(x, np.array(data[6]), label = "Work")
    plt.plot(x, np.array(data[2]), label = "Eat")
    plt.plot(x, np.array(data[5]), label = "Social")
    
    plt.legend(loc='upper center', shadow=True, fontsize='x-large')
    
    plt.grid(True)
    plt.xticks(np.arange(0, np.max(x), 6))
    plt.show() 

def plotSickness(path):
    data = read_stat_file(path, 4)
    x = data[0]

    x = (1/60) * np.array(x)
    
    plt.plot(x, np.array(data[1]), label = "Infected")
    plt.plot(x, np.array(data[2]), label = "Contagious")
    plt.plot(x, np.array(data[3]), label = "Immune")

    plt.legend(loc='upper center', shadow=True, fontsize='x-large')
    
    plt.grid(True)
    plt.xticks(np.arange(0, np.max(x), 6))
    plt.show() 
    
def plotBobby():
    time, activity = readBobbyFile("logfiles/bobby.log")
    
    # eat = sum(1 for a in activity if a == "EAT")
    # sleep = sum(1 for a in activity if a == "SLEEP")
    # work = sum(1 for a in activity if a == "WORK")
    # outdoor = sum(1 for a in activity if a == "OUTDOOR")
    # plt.pie(np.array([eat, sleep, work, outdoor]), labels = [ "Eat", "Sleep", "Work", "Outdoor" ])

    time = (1/60) * np.array(time)

    
    color = { "EAT": "#8800FF", "SLEEP": "#FF8800", "WORK": "#FF0000", "OUTDOOR": "#008800",
            "SOCIAL": "#FFC0CB", }
    colors = [color[a] for a in activity]
    plt.bar(time, height=1, width=5/60, color=colors)

    plt.grid(True)
    plt.xticks(np.arange(0, np.max(time), 6))
    plt.show()

if __name__ == "__main__":
    args = readArgs()

    if args.category == "activity":
        plotActivity("logfiles/activity.log")
    elif args.category == "bobby_needs":
        plotActivity("logfiles/bobby_needs.log")
    elif args.category == "disease":
        plotSickness("logfiles/disease.log")
    elif args.category == "bobby":
        plotBobby()
