import csv
import os

def append_list_as_row(list_of_elem, file):
    if os.stat(file).st_size == 0:
        with open(file, 'w+', newline='') as f:
            # csv_writer = csv.writer(write_obj)
            header = 'id,arrival_time,network,data_parallelism,cores,memory,batch_size,epochs,learn_rate,learn_decay'
            f.write(header + "\n")
    # Open file in append mode
    with open(file, 'a+', newline='') as write_obj:
        # Create a writer object from csv module
        csv_writer = csv.writer(write_obj)
        # Add contents of list as last row in the csv file
        csv_writer.writerow(list_of_elem)

def log_job_param(line, job):

    if "id" in line:
        job.append(line.split("id ")[1][:-1])
    if "arrival time" in line:
        job.append(line.split("arrival time ")[1][:-1])
    if "network" in line:
        job.append(line.split("network ")[1][:-1])
    if "data parallelism" in line:
        job.append(line.split("data parallelism ")[1][:-1])
    if "cores" in line:
        job.append(line.split("cores ")[1][:-1])
    if "memory" in line:
        job.append(line.split("memory ")[1][:-1])
    if "batch size" in line:
        job.append(float(line.split("batch size ")[1][:-1]))
    if "max epoch" in line:
        job.append(float(line.split("max epoch ")[1][:-1]))
    if "learning rate" in line and "learning rate decay" not in line:
        job.append(float(line.split("learning rate ")[1][:-1]))
    if "learning rate decay" in line:
        job.append(float(line.split("learning rate decay ")[1][:-1]))
        append_list_as_row(job, "job_param.csv")
        job = []
    return job


def parse():

    with open("fl-server.log", mode="r") as fl_read:
        found_line = False
        lines = fl_read.readlines()
        #id, network,system config,data parallelism,cores,memory,parameter config,batch size,max epoch,learning rate,learning rate decay
        job_param = []
        for line in lines:
            if not found_line and "Configurations for the jobs:" in line:
                found_line = True

            if found_line and not "End of configurations" in line and "Orchestrator INFO" in line:
                job_param = log_job_param(line, job_param)
            elif found_line and "End of configurations" in line in line: break

    with open("fl-server.log", mode="r") as fl_read:
        found_line = False
        lines = fl_read.readlines()
        log_lines = []
        for line in lines:
            if not found_line and "Arrival times for the jobs:" in line:
                found_line = True

            if found_line and not "End of arrival times" in line and "Orchestrator INFO" in line:
                log_lines.append(line)
            elif found_line and "End of arrival times" in line in line: break
        modified_lines = []
        for line in log_lines[1:]:
            modified_line = str.rstrip(line)
            modified_line = modified_line.split("Orchestrator INFO     ")[1]
            modified_lines.append(modified_line)

        pairs = [(modified_lines[i].split("id ")[1] + " " + modified_lines[i+1] + "\n") for i in range(0, len(modified_lines)-1, 2)]
        with open("parsed_logs_from_fl_server.txt", mode="w") as fl_write:
            fl_write.writelines(pairs)
        with open("backup_log_fl_server.txt", mode="a") as fl_backup:
            fl_backup.writelines([str(len(pairs)) + " experiments\n"])
            fl_backup.writelines(pairs)
            fl_backup.writelines(["===============================================================\n"])
        return modified_lines

if __name__ == "__main__":
    parse()