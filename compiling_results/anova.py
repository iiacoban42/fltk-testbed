import pandas as pd
import numpy as np
import pingouin as pg
from itertools import product
import os
import statsmodels.stats.multicomp

pd.set_option('display.float_format',  '{:,.5f}'.format)

frame = []

exp = '0.f'

datafile = os.getcwd() + '/compiling_results/results/'+ exp +'.csv'

df = pd.DataFrame(frame)
df = df.rename(columns = ['cores', 'memory', 'batch_size', 'epochs'])

df = pd.read_csv(datafile)

result = np.divide(df['accuracy'], df['response_time'])

anova_accuracy = pg.anova(dv='accuracy', between=['batch_size', 'epochs'], data=df,
               detailed=True)

anova_response_time = pg.anova(dv='response_time', between=['cores', 'memory', 'batch_size', 'epochs'], data=df,
               detailed=True)


with open(file= os.getcwd() + '/compiling_results/results/'+ exp +'_anova_accuracy.txt', mode='w') as anova_file:
    anova_file.write(anova_accuracy.to_string())

with open(file= os.getcwd() + '/compiling_results/results/'+ exp +'_anova_response.txt', mode='w') as anova_file:
    anova_file.write(anova_response_time.to_string())

