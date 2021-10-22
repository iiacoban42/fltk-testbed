"""Create pie chart stats"""
import matplotlib.pyplot as plt
import csv
import pickle
import time
import datetime
import os
import pandas as pd
from collections import Counter

zero = os.getcwd() + '/0.f.csv'
one_c = os.getcwd() + '/1.c.csv'
one_f = os.getcwd() + '/1.f.csv'
two_c = os.getcwd() + '/2.c.csv'
two_f = os.getcwd() + '/2.f.csv'
three_c = os.getcwd() + '/3.c.csv'
three_f = os.getcwd() + '/3.f.csv'

def create_pie_chart(labels, sizes, name):
    patches, texts = plt.pie(sizes, startangle=90)
    plt.legend(patches, labels, loc="lower center")
    plt.axis('equal')
    plt.tight_layout()
    plt.savefig(name + '.png')
    plt.show()


def generate_categorized_blocking_websites_pie():
    urls_file_path = "i2p/i2p/scraper/classified.csv"
    lables = []
    with open(urls_file_path) as csv_file:
        reader = csv.reader(csv_file)
        for i, line in enumerate(reader):
            lables.append(line[1])

    freq = dict(Counter(lables))
    freq = dict(sorted(freq.items(), key=lambda item: item[1], reverse=True))

    values = []
    lables = []
    n = sum(freq.values())
    for key, val in freq.items():
        p = round(val / n * 100, 2)
        lables.append(key + " " + str(p) + "%")
        values.append(p)
    create_pie_chart(lables, values,  "categories")

def generate_pie_charts():
    generate_blocking_proportions()
    generate_categorized_blocking_websites_pie()

generate_pie_charts()
#z_stat: 6.394, p_value: 0.000
#Reject the null hypothesis - suggest the alternative hypothesis is true
test_hypothesis_proportions()