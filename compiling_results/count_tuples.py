import pandas as pd

def count():
    df = pd.read_csv("compiling_results/job_param.csv")
    res = df.groupby(["cores","memory","batch_size","epochs"]).size()

    res.index = [tuple(x) for x in res.index]
    res = res.reset_index().set_index(0)
    print(res)

if __name__ == "__main__":
    count()