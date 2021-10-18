def parse():

    with open("trainjobs.log", mode="r") as trainjobs_read:

        lines = trainjobs_read.readlines()
        log_lines = []
        for line in lines:
            if "trainjob" in line:
                log_lines.append(line.split("trainjob-")[1][:36])
            if "Epoch" in line:
                log_lines.append(line.split("Epoch ")[1])
            if "Accuracy" in line:
                log_lines.append(line.split("Accuracy ")[1])
            if "Train loss" in line:
                log_lines.append(line.split("Train loss ")[1])
            if "Test loss" in line:
                log_lines.append(line.split("Test loss ")[1])
            if "Train time" in line:
                log_lines.append(line.split("Train time ")[1])
            if "Test time" in line:
                log_lines.append(line.split("Test time ")[1])
            if "Start time" in line:
                log_lines.append(line.split("Start time ")[1])
            if "End time" in line:
                log_lines.append(line.split("End time ")[1])


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