def parse():

    with open("compiling_results/logs-from-federation-lab-server-in-fl-server.log", mode="r") as fl_read:
        found_line = False
        lines = fl_read.readlines()
        log_lines = []
        for line in lines:
            if not found_line and "Arrival times for the jobs:" in line:
                found_line = True
            
            if found_line and not "Traceback" in line:
                log_lines.append(line)
            elif found_line and "Traceback" in line: break
        modified_lines = []
        for line in log_lines[1:]:
            modified_line = str.rstrip(line)
            modified_line = modified_line.split("Orchestrator INFO     ")[1]
            modified_lines.append(modified_line)
        
        pairs = [(modified_lines[i].split("id ")[1] + " " + modified_lines[i+1] + "\n") for i in range(0, len(modified_lines)-1, 2)]
        with open("compiling_results/parsed_logs_from_fl_server.txt", mode="w") as fl_write:
            fl_write.writelines(pairs)
        with open("compiling_results/backup_log.txt", mode="a") as fl_backup:
            fl_backup.writelines([str(len(pairs)) + " experiments\n"])
            fl_backup.writelines(pairs)
            fl_backup.writelines(["===============================================================\n"])
        return modified_lines

if __name__ == "__main__":
    parse()