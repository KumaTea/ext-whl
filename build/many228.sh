#!/usr/bin/env bash
# manylinux_2_28 wheels -- AlmaLinux 8 (glibc 2.28, GCC 14), as pypa/manylinux pins.
#
# Newer tags exist upstream but are still marked ALPHA, so 2_28 stays the
# default target here:
#   manylinux_2_34  AlmaLinux 9  (glibc 2.34)  x86_64 i686 aarch64 ppc64le s390x
#   manylinux_2_39  AlmaLinux/Rocky 10 (glibc 2.39)  aarch64 riscv64  <- riscv64 lives here now
# manylinux2014 (CentOS 7) is still published but its base has been EOL since
# 2024-06; treat it as legacy-only.
#
# The musl-wheels builder (musl-wheels/src/build.sh) is libc-agnostic --
# auditwheel picks glibc vs musl from the wheel itself -- so the same script
# works here once the toolchain below is in place.

# ====== root ======

MIRROR=mirrors.tuna.tsinghua.edu.cn

# mirrors: AlmaLinux 8 + EPEL
sed -e 's|^mirrorlist=|#mirrorlist=|g' \
    -e "s|^#\? *baseurl=https\?://repo.almalinux.org/almalinux|baseurl=https://$MIRROR/almalinux|g" \
    -i.bak /etc/yum.repos.d/almalinux*.repo

# AlmaLinux 8 GPG key rotation, 2023-12
# https://almalinux.org/blog/2023-12-20-almalinux-8-key-update/
rpm --import https://repo.almalinux.org/almalinux/RPM-GPG-KEY-AlmaLinux
dnf upgrade almalinux-release -y

dnf install epel-release -y
sed -e 's!^metalink=!#metalink=!g' \
    -e 's!^#baseurl=!baseurl=!g' \
    -e "s!https\?://download\.fedoraproject\.org/pub/epel!https://$MIRROR/epel!g" \
    -e "s!https\?://download\.example/pub/epel!https://$MIRROR/epel!g" \
    -i /etc/yum.repos.d/epel{,-testing}.repo

dnf install -y wget curl nano gcc-toolset-14 openssh-server openssh-clients \
               tar bzip2 xz rsync patchelf
dnf clean all
systemctl start sshd
systemctl enable sshd

# ====== non-root user ======

PYPI=https://$MIRROR/pypi/web/simple
export UV_DEFAULT_INDEX=$PYPI PIP_INDEX_URL=$PYPI

curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH="$HOME/.local/bin:$PATH"

# uv manages PyPy too, so no more hand-unpacking tarballs from downloads.python.org.
# (CPython 3.14/3.15 and the free-threaded builds come from the same place.)
uv python install 3.11 3.12 3.13 3.14 3.13t 3.14t pypy3.11
uv tool install auditwheel

# ====== example: cryptg ======

scl enable gcc-toolset-14 bash   # everything below runs inside this shell

OUT_DIR=$HOME/out
RAW_DIR=$HOME/raw
mkdir -p "$OUT_DIR" "$RAW_DIR"

for PV in 3.11 3.12 3.13 3.14 3.13t 3.14t pypy3.11; do
    uv venv -p "$PV" --seed "/tmp/v$PV" || continue
    # --no-binary <pkg> compiles the sdist; build deps still install as wheels.
    # Beats scraping ~/.cache for whatever uv happened to build.
    "/tmp/v$PV/bin/pip" wheel --no-deps --no-binary cryptg 'cryptg==0.6.0' -w "$RAW_DIR"
done

for whl in "$RAW_DIR"/*.whl; do
    auditwheel repair --strip -w "$OUT_DIR" "$whl"
done

auditwheel show "$OUT_DIR"/*.whl | grep -E 'platform tag'

uv cache clean
rm -rf "$RAW_DIR" /tmp/v3.* /tmp/vpypy*
