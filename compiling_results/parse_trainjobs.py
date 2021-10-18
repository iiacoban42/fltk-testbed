import csv

def append_list_as_row(list_of_elem, file):
    # Open file in append mode
    with open(file, 'a+', newline='') as write_obj:
        # Create a writer object from csv module
        csv_writer = csv.writer(write_obj)
        # Add contents of list as last row in the csv file
        csv_writer.writerow(list_of_elem)

def parse():

    with open("trainjobs.log", mode="r") as trainjobs_read:

        lines = trainjobs_read.readlines()
        log_lines = []
        # ['job_id', start time, end time, accuracy, train loss, test loss]
        job = []
        for line in lines:
            if "trainjob" in line:
                trainjob = line.split("trainjob-")[1][:36]
                log_lines.append(trainjob)
                job.append(trainjob)
            if "Start time" in line:
                start_time = line.split("Start time ")[1]
                log_lines.append(start_time)
                job.append(start_time[:-1])
            if "End time" in line:
                end_time = line.split("End time ")[1]
                log_lines.append(end_time)
                job.append(end_time[:-1])
            if "Accuracy" in line:
                accuracy = line.split("Accuracy ")[1]
                job.append(float(accuracy))
            if "Train loss" in line:
                train_loss = line.split("Train loss ")[1]
                job.append(float(train_loss))
            if "Test loss" in line:
                test_loss = line.split("Test loss ")[1]
                job.append(float(test_loss))
                append_list_as_row(job, "ml_results.csv")
                job = []

        modified_lines = []
        for line in log_lines:
            modified_line = str.rstrip(line)
            modified_lines.append(modified_line)

        triples = [(modified_lines[i] + " " + modified_lines[i+1] + " " + modified_lines[i+2] + "\n") for i in range(0, len(modified_lines)-2, 3)]
        with open("parsed_logs_from_trainjobs.txt", mode="w") as trainjobs_write:
            trainjobs_write.writelines(triples)
        with open("backup_log_trainjobs.txt", mode="a") as trainjobs_backup:
            trainjobs_backup.writelines([str(len(triples)) + " experiments\n"])
            trainjobs_backup.writelines(triples)
            trainjobs_backup.writelines(["============================================================================================================\n"])
if __name__ == "__main__":
    parse()
