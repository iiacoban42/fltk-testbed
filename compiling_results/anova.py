import pandas as pd
import researchpy as rp
import seaborn as sns
import numpy as np

import statsmodels.api as sm
from statsmodels.formula.api import ols
import statsmodels.stats.multicomp

# responce_time = [3.8455, 3.8191, 3.8634, 3.5061, 3.4598, 3.5469, 3.6727, 3.6933, 3.6498, 3.7082, 3.7410, 3.6761, 3.8330, 3.8056, 3.8578,
#             4.0807, 4.0717, 4.1164, 3.7095, 3.7507, 3.6635, 3.9735, 3.9510, 3.9984, 3.7492, 3.7743, 3.7127, 4.0879, 4.0790, 4.1131,
#             4.4633, 4.4321, 4.4779, 3.9523, 3.9066, 3.9857, 4.2953, 4.2866, 4.3247, 4.3491, 4.3636, 4.3313, 4.4558, 4.4289, 4.4851,
#             3.9958, 3.9641, 4.0015, 3.6184, 3.6291, 3.6091, 3.8506, 3.8440, 3.8246, 3.7288, 3.7585, 3.6959, 3.9914, 3.9688, 4.0100]
# df = pd.DataFrame({'Responce_Time': responce_time,
#                    'Cores': np.repeat([4, 8], 30),
#                    'Memory': np.repeat([8, 16], 30)})
# data = pd.read_csv(datafile)
#####################################################################
# df.to_csv(datafile)
datafile = "compiling_results/exp_data.csv"
df = pd.read_csv(datafile)
model = ols('Responce_Time ~ C(Cores)*C(Memory)', df).fit()

# Seeing if the overall model is significant
print(f"Overall model F({model.df_model: .0f},{model.df_resid: .0f}) = {model.fvalue: .3f}, p = {model.f_pvalue: .4f}")

res = sm.stats.anova_lm(model, typ=2)
res