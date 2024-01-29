import os

AUTHOR = 'KumaTea'
PROJECTS = [
    'pypy-wheels',
    'riscv-wheels',
    'ext-whl',
    'NextBot',
]

if os.name == 'nt':
    WORKDIR = '..'
else:
    WORKDIR = '.'
