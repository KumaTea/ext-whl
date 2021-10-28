#!/usr/bin/env bash

set -ex

# deps

sed -i 's@http://deb.debian.org/debian@https://mirrors.tuna.tsinghua.edu.cn/debian@g' /etc/apt/sources.list
sed -i 's@http://security.debian.org/debian-security@https://mirrors.tuna.tsinghua.edu.cn/debian-security@g' /etc/apt/sources.list
apt update
apt install -y pkg-config libhdf5-dev
apt install -y gfortran libopenblas-dev liblapack-dev
ln -s /usr/include/locale.h /usr/include/xlocale.h || :

pip install -U -v -r /root/packages-stdln.txt -f https://ext.kmtea.eu/wheels.html -f http://192.168.2.225:10378/
pip install -U -v -r /root/packages-deps.txt -f https://ext.kmtea.eu/wheels.html -f https://torch.kmtea.eu/whl/stable.html -f https://tf.kmtea.eu/whl/stable.html -f http://192.168.2.225:10378/

mkdir /root/whl
cp -a $(find /root/.cache/pip | grep whl | tr '\n' ' ') /root/whl/ || echo "No new whl is built!"
