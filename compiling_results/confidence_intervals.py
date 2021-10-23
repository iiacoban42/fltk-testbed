from pyDOE2 import *
import pandas as pd
import os
from scipy import stats

def ci():
    design = ff2n(4)

    cores_column = [row[0] for row in design]
    memory_column = [row[1] for row in design]
    batch_column = [row[2] for row in design]
    epochs_column = [row[3] for row in design]    

    exp_result = '0.f_anova_accuracy'

    datafile_result = os.getcwd() + '/compiling_results/results/'+ exp_result +'.txt'

    with open(datafile_result, "r") as f:
        lines = f.readlines()
        last = lines[len(lines)-1]
        ss_e = float(last.split("Residual ")[1].split(" ")[0])
    
    exp = '0.f'

    datafile = os.getcwd() + '/compiling_results/results/'+ exp +'.csv'

    df = pd.read_csv(datafile)

    

    res = df.groupby(["cores","memory","batch_size","epochs"]).mean()
    # print(res)

    # res.to_csv("compiling_results/res.csv")

    # print(res)
    measurements = res['accuracy'].tolist()

    q_cores = sum([1/16* i*j for i,j in zip(measurements, cores_column)])
    q_memory = sum([1/16* i*j for i,j in zip(measurements, memory_column)])
    q_batch = sum([1/16* i*j for i,j in zip(measurements, batch_column)])
    q_epochs = sum([1/16* i*j for i,j in zip(measurements, epochs_column)])

    alpha = 0.1
    dof = 2**4 * 2

    s_e = np.sqrt(ss_e/dof)

    s_qi = s_e/(2**4*3)

    t = stats.t.ppf(1-alpha/2, dof)

    ci_cores = [q_cores - t*s_qi, q_cores + t*s_qi]
    ci_memory = [q_memory - t*s_qi, q_memory + t*s_qi]
    ci_batch = [q_batch - t*s_qi, q_batch + t*s_qi]
    ci_epochs = [q_epochs - t*s_qi, q_epochs + t*s_qi]

    print("cores " + str(ci_cores))
    print("memory " + str(ci_memory))
    print("batch " + str(ci_batch))
    print("epochs " + str(ci_epochs))
    

if __name__ == "__main__":
    ci()