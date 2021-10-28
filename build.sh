#!/usr/bin/env bash

set -ex

#mkdir whl || :

cd docker
docker build --pull -t kumatea/ext:py310 -f py310/Dockerfile .
docker build --pull -t kumatea/ext:py39 -f py39/Dockerfile .
docker build --pull -t kumatea/ext:py38 -f py38/Dockerfile .
docker build --pull -t kumatea/ext:py37 -f py37/Dockerfile .
docker build --pull -t kumatea/ext:py36 -f py36/Dockerfile .

docker image prune

mkdir -p whl
python3 local-whl.py &
FLASK_PID=$!

docker run -it --name py310e kumatea/ext:py310 bash /root/build-wheels.sh
docker cp py310e:/root/whl .
docker rm py310e

docker run -it --name py39e kumatea/ext:py39 bash /root/build-wheels.sh
docker cp py39e:/root/whl .
docker rm py39e

docker run -it --name py38e kumatea/ext:py38 bash /root/build-wheels.sh
docker cp py38e:/root/whl .
docker rm py38e

docker run -it --name py37e kumatea/ext:py37 bash /root/build-wheels.sh
docker cp py37e:/root/whl .
docker rm py37e

docker run -it --name py36e kumatea/ext:py36 bash /root/build-wheels.sh
docker cp py36e:/root/whl .
docker rm py36e

kill $FLASK_PID
