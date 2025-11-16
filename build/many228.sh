#!/usr/bin/env bash

# using Almalinux 8 as pypa/manylinux indicates for manylinux_2_28

# ====== root ======

# mirrors
sed -e 's|^mirrorlist=|#mirrorlist=|g' -e 's|^# baseurl=https://mirrors.tencent.com|baseurl=https://repo.almalinux.org|g' -i.bak /etc/yum.repos.d/almalinux*.repo

# fixing Almalinux 8 GPG issue
# https://almalinux.org/blog/2023-12-20-almalinux-8-key-update/
rpm --import https://repo.almalinux.org/almalinux/RPM-GPG-KEY-AlmaLinux
dnf upgrade almalinux-release -y

dnf install epel-release -y
sed -e 's!^metalink=!#metalink=!g'     -e 's!^#baseurl=!baseurl=!g'     -e 's!https\?://download\.fedoraproject\.org/pub/epel!https://mirrors.bfsu.edu.cn/epel!g'     -e 's!https\?://download\.example/pub/epel!https://mirrors.bfsu.edu.cn/epel!g'     -i /etc/yum.repos.d/epel{,-testing}.repo

dnf install wget curl nano gcc-toolset-14 openssh-server openssh-clients tar bzip2 rsync -y
dnf clean all
systemctl start sshd
systemctl enable sshd

# ====== non-root user ======

curl -LsSf https://astral.sh/uv/install.sh | sh
cd /tmp
wget https://downloads.python.org/pypy/pypy3.11-v7.3.20-linux64.tar.bz2
tar -xvjf pypy3.11-v7.3.20-linux64.tar.bz2
mv pypy3.11-v7.3.20-linux64 /opt/pypy
sudo mv /opt/pypy3.11-v7.3.20-linux64 /opt/pypy
sudo ln -s /opt/pypy/bin/pypy /usr/local/bin/pypy
sudo ln -s /opt/pypy/bin/pypy3 /usr/local/bin/pypy3

# ====== example ======

scl enable gcc-toolset-14 bash
uv init py314 --python 3.14
cd py314
uv add auditwheel patchelf
uv add tgcrypto

# auditwheel repair

WHL_FILES=$(find ~/.cache/uv | grep whl)
OUT_DIR=/home/kuma/out
for whl in $WHL_FILES; do
    uv run auditwheel repair -w $OUT_DIR $whl
done

# pypy

pypy3 -m ensurepip
pypy3 -m venv pp311
cd pp311
source bin/activate
pip install auditwheel patchelf
pip install tgcrypto

WHL_FILES=$(find ~/.cache/pip | grep whl)
OUT_DIR=/home/kuma/out
for whl in $WHL_FILES; do
    auditwheel repair -w $OUT_DIR $whl
done

uv clean all
pip cache purge
rm -rf ~/.cache
