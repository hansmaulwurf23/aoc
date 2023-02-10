#!/bin/bash
containerName=aoc

if [ $(docker ps -q -f name=$containerName | wc -l) -eq 1 ]; then
	echo 'containter already running...'
	exit
fi

if [ $(docker ps -q -a -f name=$containerName | wc -l) -eq 0 ]; then
	echo 'need build...'
	docker build -t aoc . && \
	docker run -ti --rm -v $(pwd):/aoc -m 8G -e PYTHONPATH=/aoc/aopython/ --name $containerName $containerName:latest /bin/bash 
else
	echo 'found. starting...'
	docker start aoc
fi


