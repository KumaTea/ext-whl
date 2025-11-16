#!/bin/ash

# using Alpine 3.22 as pypa/manylinux indicates for musllinux_1_2

# ====== root ======

# mirrors
sed -i 's#https\?://dl-cdn.alpinelinux.org/alpine#https://mirrors.tuna.tsinghua.edu.cn/alpine#g' /etc/apk/repositories
apk add alpine-sdk curl wget nano openssh sudo rsync
apk cache clean
service sshd start
rc-update add sshd

# ====== non-root user ======

# install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# ====== example ======

uv init py314 --python 3.14
cd py314
uv add auditwheel patchelf
uv add tgcrypto

# auditwheel repair

WHL_FILES=$(find ~/.cache | grep whl)
OUT_DIR=/home/kuma/out
for whl in $WHL_FILES; do
    uv run auditwheel repair -w $OUT_DIR $whl
done

uv clean all
rm -rf ~/.cache
