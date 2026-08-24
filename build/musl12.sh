#!/bin/sh
# musllinux_1_2 wheels.
#
# The maintained, automated version of this lives in the musl-wheels repo:
#
#     musl-wheels/docker/Dockerfile   alpine:3.22 + toolchain + uv + auditwheel
#     musl-wheels/src/build.sh        build + auditwheel repair + import test
#     musl-wheels/build.ps1           one command from Windows, wheels come back
#
#     .\build.ps1 'cryptg==0.6.0'
#
# What follows is the same recipe by hand, for when a package needs extra
# system libraries and you want a shell in the container.
#
# Alpine 3.22 on purpose: that is what pypa/manylinux pins for musllinux_1_2
# (musl 1.2.5, GCC 14). NOT quay.io/pypa/musllinux_1_2_x86_64 -- that image
# ships every interpreter prebuilt and is several GB; this comes out ~900 MB
# with the Rust toolchain, and the interpreters live in a cached volume.

# ====== host ======

docker run -it --name musl \
    -v musl-uv-python:/opt/uv/python \
    -v "$HOME/out:/out" \
    alpine:3.22 sh

# ====== in the container, as root ======

MIRROR=mirrors.tuna.tsinghua.edu.cn
PYPI=https://$MIRROR/pypi/web/simple

sed -i "s#https\?://dl-cdn.alpinelinux.org/alpine#https://$MIRROR/alpine#g" /etc/apk/repositories
apk update
apk add --no-cache build-base linux-headers musl-dev cmake ninja pkgconf \
                   curl git unzip wget xz patchelf \
                   libffi-dev openssl-dev zlib-dev bzip2-dev xz-dev
apk add --no-cache rust cargo    # cryptg, cryptography, pydantic-core, ...

# uv from the PyPI mirror (astral.sh redirects to GitHub release assets, slow)
rel=$(curl -fsSL "$PYPI/uv/" | grep -o 'href="[^"]*musllinux_1_1_x86_64\.whl[^"]*"' \
      | sed 's/href="//;s/"$//' | sort -V | tail -1)
url="${PYPI%/simple}/${rel#../../}"; url="${url%%#*}"
mkdir -p /tmp/uvw && cd /tmp/uvw && curl -fsSL -o uv.whl "$url" && unzip -q uv.whl
install -m755 "$(find . -type f -name uv | head -1)" /usr/local/bin/uv
cd / && rm -rf /tmp/uvw

export UV_DEFAULT_INDEX=$PYPI PIP_INDEX_URL=$PYPI
export UV_PYTHON_INSTALL_DIR=/opt/uv/python UV_TOOL_DIR=/opt/uv/tools
export RUSTFLAGS="-C target-feature=-crt-static"   # keep the cdylib dynamic

# uv ships musl CPython builds -- this is what makes 3.11..3.15 on Alpine easy.
# (PyPy has no musl builds, so musllinux is CPython-only.)
uv python install 3.11 3.12 3.13 3.14 3.13t 3.14t
uv tool install auditwheel
ln -sf /opt/uv/tools/auditwheel/bin/auditwheel /usr/local/bin/auditwheel

# ====== example: cryptg ======

for PV in 3.11 3.12 3.13 3.14 3.13t 3.14t; do
    uv venv -p "$PV" --seed "/tmp/v$PV"
    # --no-binary <pkg> forces the sdist to be compiled; deps still come as wheels
    "/tmp/v$PV/bin/pip" wheel --no-deps --no-binary cryptg 'cryptg==0.6.0' -w /tmp/raw
done

for whl in /tmp/raw/*.whl; do
    auditwheel repair --strip -w /out "$whl"    # linux_x86_64 -> musllinux_1_2_x86_64
done

uv cache clean
rm -rf /root/.cache /tmp/raw /tmp/v3.*
