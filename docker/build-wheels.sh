#!/usr/bin/env bash

set -ex

# deps

sed -i 's@http://deb.debian.org/debian@https://mirrors.matrix.moe/debian@g' /etc/apt/sources.list
sed -i 's@http://security.debian.org/debian-security@https://mirrors.matrix.moe/debian-security@g' /etc/apt/sources.list
apt update
apt install -y pkg-config libhdf5-dev
ln -s /usr/include/locale.h /usr/include/xlocale.h || :

if [ $(uname -m) = 'armv7l' ]; then
  sed -i 's/scikit-learn//g' /root/packages-stdln.txt
fi

pip install -U -v -r /root/packages-stdln.txt -f https://ext.kmtea.eu/wheels.html -f https://torch.kmtea.eu/whl/stable.html

if [ $(uname -m) = 'aarch64' ]; then
  pip install -U -v -r /root/packages-deps.txt -f https://ext.kmtea.eu/wheels.html -f https://torch.kmtea.eu/whl/stable.html -f https://tf.kmtea.eu/whl/stable.html
fi

mkdir /root/whl
cp -a $(find /root/.cache/pip | grep whl | tr '\n' ' ') /root/whl/ || echo "No new whl is built!"
