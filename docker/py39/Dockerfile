FROM python:3.9

RUN set -ex \
        \
        && pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple \
        && python3 -m pip install -U pip setuptools wheel \
        && rm -rf /root/.cache/*

COPY packages-deps.txt /root/
COPY packages-stdln.txt /root/
COPY build-wheels.sh /root/

CMD ["/bin/bash"]
