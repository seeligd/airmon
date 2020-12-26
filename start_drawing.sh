#/bin/bash
while true
do
	python convert_aqi.py < samples.csv
	echo $(date) drawing
	python draw_graph.py
	echo $(date) done
	sleep 60
done
