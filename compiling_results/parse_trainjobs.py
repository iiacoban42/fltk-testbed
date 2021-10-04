def parse():

    with open("trainjobs.log", mode="r") as trainjobs_read:
        
        lines = trainjobs_read.readlines()
        log_lines = []
        for line in lines:
            if "trainjob" in line:
                log_lines.append(line)
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