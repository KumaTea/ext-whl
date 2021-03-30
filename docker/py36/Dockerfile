FROM python:3.6

RUN set -ex \
        \
        && pip config set global.index-url https://mirrors.vmatrix.org.cn/pypi/web/simple \
        && python3 -m pip install -U pip setuptools wheel \
        && rm -rf /root/.cache/*

COPY packages-deps.txt /root/
COPY packages-stdln.txt /root/
COPY build-wheels.sh /root/

CMD ["/bin/bash"]
