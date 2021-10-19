python3 parse_fl_server.py
echo "parsed fl-server logs"
python3 parse_trainjobs.py
echo "parsed trainjob logs"
python3 merge_statistics.py
echo "final results generated in statistics.txt"