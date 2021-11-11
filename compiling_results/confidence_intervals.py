from pyDOE2 import *
import pandas as pd
import os
from scipy import stats

def ci(exp, metric):
    if '1' in exp:
        design = ff2n(2)
        
        batch_column = [row[0] for row in design]
        epochs_column = [row[1] for row in design]
    else:
        design = ff2n(4)
        cores_column = [row[0] for row in design]
        memory_column = [row[1] for row in design]
        batch_column = [row[2] for row in design]
        epochs_column = [row[3] for row in design]     
    

    exp_result = '0.f_anova_' + metric

    datafile_result = os.getcwd() + '/compiling_results/results/'+ exp_result +'.txt'

    with open(datafile_result, "r") as f:
        lines = f.readlines()
        last = lines[len(lines)-1]
        value = last.split()[2]
        if ',' in value:
            value = value.replace(',','')
        ss_e = float(value)

    datafile = os.getcwd() + '/compiling_results/results/'+ exp +'.csv'

    df = pd.read_csv(datafile)

    res = df.groupby(["cores","memory","batch_size","epochs"]).mean()

    if metric == 'response':
        measurements = res[metric+'_time'].tolist()
    else: measurements = res[metric].tolist()

    if not '1' in exp:    
        q_cores = 1/len(measurements)*sum([i*j for i,j in zip(measurements, cores_column)])
        q_memory = 1/len(measurements)*sum([i*j for i,j in zip(measurements, memory_column)])
    q_batch = 1/len(measurements)*sum([i*j for i,j in zip(measurements, batch_column)])
    q_epochs = 1/len(measurements)*sum([i*j for i,j in zip(measurements, epochs_column)])

    alpha = 0.05
    dof = 2**np.sqrt(len(measurements)) * 2

    s_e = np.sqrt(ss_e/dof)

    s_qi = s_e/(2**np.sqrt(len(measurements))*3)

    t = stats.t.ppf(1-alpha/2, dof)

    if not '1' in exp:
        ci_cores = [q_cores - t*s_qi, q_cores + t*s_qi]
        ci_memory = [q_memory - t*s_qi, q_memory + t*s_qi]
        ci_batch = [q_batch - t*s_qi, q_batch + t*s_qi]
        ci_epochs = [q_epochs - t*s_qi, q_epochs + t*s_qi]

        ls = ["cores " + str(ci_cores)+ "\n", \
            "memory " + str(ci_memory)+ "\n","batch " + str(ci_batch)+ "\n","epochs " + str(ci_epochs)]
    else:
        ci_batch = [q_batch - t*s_qi, q_batch + t*s_qi]
        ci_epochs = [q_epochs - t*s_qi, q_epochs + t*s_qi]

        ls = ["batch " + str(ci_batch)+ "\n","epochs " + str(ci_epochs)]

    with open("compiling_results/results/" + exp +"_"+ metric +"_ci.txt", "w+") as fl:
        fl.writelines(ls)
     
    print("compiling_results/results/" + exp +"_"+ metric +"_ci.txt successfully created")
    

if __name__ == "__main__":

    for metric in ['accuracy', 'response']:
        for exp in ['0.f','1.c','1.f','2.c','2.f','3.c','3.f']:
            ci(exp,metric)
