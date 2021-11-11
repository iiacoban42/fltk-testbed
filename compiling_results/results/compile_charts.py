"""Create boxplots"""
import pandas as pd
import numpy as np
from itertools import product
import os
import statsmodels.stats.multicomp
import matplotlib.pyplot as plt


def get_boxplot(exp, data, labels):

    fig = plt.figure(figsize =(10, 7))
    # Creating axes instance

    # Creating plot
    bp = plt.boxplot(data)

    # show plot
    plt.savefig(exp+".jpeg")
    plt.show()


def get_data(exp, exp_result, factor):
    # pd.set_option('display.float_format',  '{:,.5f}'.format)
    datafile = os.getcwd() + '/compiling_results/results/'+ exp +'.csv'

    df = pd.read_csv(datafile)

    factor_config = df[factor].unique()

    data = []
    boxplot_df = pd.DataFrame([])

    for fact in factor_config:
        # filter rows by factor config
        new_df = df[df[factor]==fact]
        # get accuracy/response time
        new_data = new_df[exp_result]
        data.append(new_data)
        # print(fact)

        boxplot_df[fact] = new_data

    daaata = {
        factor_config[0]: data[0],
        factor_config[1]: data[1]

    }
    # boxplot_df[factor_config[0]] =
    # boxplot_df[factor_config[1]] = data[1]

    boxplot_df = pd.DataFrame(daaata)
    print(data)
    print(boxplot_df)

    myFig = plt.figure()
    bp = boxplot_df.boxplot()
    myFig.savefig(exp+".jpg", format="jpg")


exp = '0.f'
exp_result = {
        'A': "accuracy",
        'T': "response_time"
    }
factors = {
        'C': "cores",
        'M': "memory",
        'B': "batch_size",
        'E': "epochs"
    }

get_data(exp, exp_result['T'], factors['E'])