import os

AUTHOR = 'KumaTea'
PROJECTS = [
    'pypy-wheels',
    'riscv-wheels',
    'musl-wheels',
    'ext-whl',
    'NextBot',
    'pytorch-riscv64',
]

if os.path.isfile('conf.py'):
    WORKDIR = '..'
else:
    WORKDIR = '.'

LOCAL_WHL_DIR = r'E:\Cache\whl'
