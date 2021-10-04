import datetime

def merge():

    with open("parsed_logs_from_fl_server.txt", mode="r") as fl:
        fl_lines = fl.readlines()

        with open("parsed_logs_from_trainjobs.txt", mode="r") as tr:
            tr_lines = tr.readlines()

            valid_ids = []
            job_start_times = []
            job_finish_times = []
            for tr_line in tr_lines:
                valid_ids.append(tr_line.split(" ")[0])
                job_start_times.append(tr_line.split(" ")[1] + " " + tr_line.split(" ")[2])
                job_finish_times.append(str.rstrip(tr_line.split(" ")[3] + " " + tr_line.split(" ")[4]))
            
            job_arrival_times = {}
            for fl_line in fl_lines:
                id = fl_line.split(" ")[0]
                if id in valid_ids:
                    index = valid_ids.index(id)
                    job_arrival_times[index] = str.rstrip(fl_line.split(" ")[1] + " " + fl_line.split(" ")[2])

    arrivals = list({key:job_arrival_times[key] for key in sorted(job_arrival_times.keys())}.values())

    datetime_arrivals = [datetime.datetime.strptime(i, "%Y-%m-%d %H:%M:%S.%f") for i in arrivals]
    datetime_starts = [datetime.datetime.strptime(i, "%Y-%m-%d %H:%M:%S.%f") for i in job_start_times]
    datetime_finishes = [datetime.datetime.strptime(i, "%Y-%m-%d %H:%M:%S.%f") for i in job_finish_times]

    time_in_queue = [(s - a).total_seconds() * 1000 for s,a in zip(datetime_starts,datetime_arrivals)]
    time_processing = [(f - s).total_seconds() * 1000 for f,s in zip(datetime_finishes,datetime_starts)]
    response_time = [(f - a).total_seconds() * 1000 for f,a in zip(datetime_finishes,datetime_arrivals)]

    lines = []
    for i, id in enumerate(valid_ids):
        lines.append("=======================================\n")
        lines.append("Job with id " + id + "\n")
        lines.append("Arrived in system at  " + arrivals[i] + "\n")
        lines.append("Started executing at  " + job_start_times[i]+ "\n")
        lines.append("Finished executing at " + job_finish_times[i]+ "\n\n")
        lines.append("Time spent in queue   " + str(time_in_queue[i])+ "\n")
        lines.append("Time spent processing " + str(time_processing[i])+ "\n")
        lines.append("Response time         " + str(response_time[i])+ "\n")

    with open("statistics.txt", mode="w") as stats:
        stats.writelines(lines)

if __name__ == "__main__":
    merge()