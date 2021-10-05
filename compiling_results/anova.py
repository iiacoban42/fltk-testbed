import pandas as pd
# import researchpy as rp
# import seaborn as sns
import numpy as np
import pingouin as pg
from itertools import product

# import statsmodels.api as sm
# from statsmodels.formula.api import ols
import statsmodels.stats.multicomp
datafile = "compiling_results/exp_data.csv"
response_time = [   208241.587,223431.035,103231.234,204231.523,203243.571,232291.545,202265.943,201234.432,324231.677,238231.211,
                    234222.741,203430.547,208231.237,201332.532,248221.765,254201.543,203430.387,234231.537,255231.485,458231.237,
                    245231.237,124342.324,108631.596,242441.111,205633.237,218223.556,202231.000,205532.090,205231.587,456231.652,
                    265223.457,223434.934,208000.554,232237.557,202554.345,233030.576,202345.332,212245.565,205531.350,208231.094,
                    204331.567,204440.023,308231.930,234239.843,200012.007,206564.587,153321.587,209643.589                      ]
df = pd.DataFrame(data=[['4', '8', '128', '0.01'], 
                        ['8', '16', '256', '0.05']],
                  columns=['Cores', 'Memory', 'Batch', 'Learn'])
                  
combinations = list(product(df['Cores'], df['Memory'], df['Batch'], df['Learn']))

combinations3 = []

for comb in combinations:
    combinations3.append(comb)
    combinations3.append(comb)
    combinations3.append(comb)

frame = []

for i, comb in enumerate(combinations3):
    frame.append((response_time[i], *comb))
    
# # print(frame)
renaming = {
    0:"Response_Time",
    1:"Cores",
    2:"Memory",
    3:"Batch",
    4:"Learn"
}
df = pd.DataFrame(frame)
df = df.rename(columns = renaming)

df.to_csv(datafile)

df = pd.read_csv(datafile)
# # # model = ols('Response_Time ~ C(Cores, Sum) + C(Memory, Sum) + C(Batch, Sum) + C(Learn, Sum) + \
# # #             C(Cores, Sum):C(Memory, Sum) + C(Cores, Sum):C(Batch, Sum) + C(Cores, Sum):C(Learn, Sum) + C(Memory, Sum):C(Batch, Sum) + C(Batch, Sum):C(Learn, Sum) +\
# # #             C(Cores, Sum):C(Memory, Sum):C(Batch, Sum) + C(Cores, Sum):C(Memory, Sum):C(Learn, Sum) + C(Memory, Sum):C(Batch, Sum):C(Learn, Sum) +\
# # #             C(Cores, Sum):C(Memory, Sum):C(Batch, Sum):C(Learn, Sum)', df).fit()

# anova = pg.anova(dv='Response_Time', between=['Cores', 'Memory', 'Batch', 'Learn'], data=df,
#                detailed=True)

# print(anova)

# # # # Seeing if the overall model is significant
# # # print(f"Overall model F({model.df_model: .0f},{model.df_resid: .0f}) = {model.fvalue: .3f}, p = {model.f_pvalue: .4f}")

# # # res = sm.stats.anova_lm(model, typ=3)
# # # res