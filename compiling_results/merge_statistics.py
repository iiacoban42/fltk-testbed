import datetime
import pandas as pd

def merge():

    server_df = pd.read_csv("job_param.csv")
    ml_df = pd.read_csv("ml_results.csv")

    merged_frame = pd.merge(left=server_df, right=ml_df, left_on='id', right_on='id')

    arrivals = merged_frame['arrival_time'].tolist()
    starts = merged_frame['start_time'].tolist()
    finishes = merged_frame['end_time'].tolist()

    datetime_arrivals = [datetime.datetime.strptime(i, "%Y-%m-%d %H:%M:%S.%f") for i in arrivals]
    datetime_starts = [datetime.datetime.strptime(i, "%Y-%m-%d %H:%M:%S.%f") for i in starts]
    datetime_finishes = [datetime.datetime.strptime(i, "%Y-%m-%d %H:%M:%S.%f") for i in finishes]

    service_times = [(f - s).total_seconds() * 1000 for f,s in zip(datetime_finishes,datetime_starts)]
    times_in_queue = [(s - a).total_seconds() * 1000 for s,a in zip(datetime_starts,datetime_arrivals)]
    response_times = [(f - a).total_seconds() * 1000 for f,a in zip(datetime_finishes,datetime_arrivals)]

    merged_frame['service_time'] = service_times
    merged_frame['queue_time'] = times_in_queue
    merged_frame['response_time'] = response_times
    merged_frame.to_csv("exp_data.csv")

if __name__ == "__main__":
    merge()