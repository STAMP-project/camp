#!/bin/bash -xe


mkdir results
echo "Starting experiments"
for (( i = 0; i < 10; i++ )); do
	echo "Copying files"
	cp experiments/features_${i}.yml features.yml
	cp experiments/images_${i}.yml images.yml
	echo "Creating result folder"
	mkdir results/results_${i}
	for (( j = 0; j < 10; j++ )); do
		docker run -it -v $(pwd):/root/workingdir camp-tool:latest /bin/bash start.sh | tee -a results/results_${i}/output_${j}
	done
done
echo "All experiments are completed!"