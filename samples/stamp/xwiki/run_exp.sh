#!/bin/bash

mkdir results
echo "Sarting experiment"
for (( i = 0; i < 6; i++ )); do
	mkdir results/results_${i}
	for (( j = 0; j < 1; i++ )); do
		docker run -it -v $(pwd):/root/workingdir camp-tool:latest /bin/bash start.sh | tee -a resuls/resuls_${i}/output_${j}
	done
done