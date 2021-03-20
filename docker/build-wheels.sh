#!/usr/bin/env bash

set -ex

# pip config set global.index-url https://mirrors.matrix.moe/pypi/web/simple
pip install -U -r /root/packages.txt -f https://ext.maku.ml/wheels.html -f https://torch.maku.ml/whl/stable.html
mkdir /root/whl
cp -a $(find /root/.cache/pip | grep whl | tr '\n' ' ') /root/whl/ || echo "No new whl is built!"
