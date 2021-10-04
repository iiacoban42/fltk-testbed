./log_deployment.sh "trainjob" > trainjobs.log
echo "got trainjob logs"
./log_deployment.sh "fl-server" > fl-server.log
echo "got fl-server logs"
python3 parse_fl_server.py
echo "parsed fl-server logs"
python3 parse_trainjobs.py
echo "parsed trainjob logs"
python3 merge_statistics.py
echo "final results generated in statistics.txt"