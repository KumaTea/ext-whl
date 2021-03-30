#!/usr/bin/env bash

set -ex

# pip config set global.index-url https://mirrors.vmatrix.org.cn/pypi/web/simple
pip install -U -v -r /root/packages-stdln.txt -f https://ext.maku.ml/wheels.html -f https://torch.maku.ml/whl/stable.html
pip install -U -v -r /root/packages-deps.txt -f https://ext.maku.ml/wheels.html -f https://torch.maku.ml/whl/stable.html
mkdir /root/whl
cp -a $(find /root/.cache/pip | grep whl | tr '\n' ' ') /root/whl/ || echo "No new whl is built!"
