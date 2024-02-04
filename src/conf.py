import os

AUTHOR = 'KumaTea'
PROJECTS = [
    'pypy-wheels',
    'riscv-wheels',
    'ext-whl',
    'NextBot',
    'pytorch-riscv64',
]

if os.name == 'nt':
    WORKDIR = '..'
else:
    WORKDIR = '.'
