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

if os.name == 'nt':
    WORKDIR = '..'
else:
    WORKDIR = '.'

LOCAL_WHL_DIR = r'E:\Cache\whl'
