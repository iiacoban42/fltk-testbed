./log_deployment.sh "trainjob" > trainjobs.log
./log_deployment.sh "fl-server" > fl-server.log
python3 parse_fl_server.py
python3 parse_trainjobs.py