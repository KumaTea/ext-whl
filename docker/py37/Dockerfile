FROM python:3.7

RUN set -ex \
        \
        && pip config set global.index-url https://mirrors.matrix.moe/pypi/web/simple \
        && python3 -m pip install -U pip setuptools wheel \
        && rm -rf /root/.cache/*

COPY packages.txt /root/
COPY build-wheels.sh /root/

CMD ["/bin/bash"]
