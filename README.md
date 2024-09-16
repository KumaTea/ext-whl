# ext-whl
Extended Python wheels (whl)

This project provides pre-built wheels of popular packages.

### Add to pip

```bash
pip config set global.extra-index-url https://ext.kmtea.eu/simple
```

### Temporary use

```bash
pip install <package> --prefer-binary --extra-index-url https://ext.kmtea.eu/simple
```

The `--prefer-binary` option is to ensure that
once the source updates, the binary will still be used.
You may dismiss it at your will.

An alternative way is to use the `--find-links` option,
which is not recommended because the size of the index is large:

```bash
pip install <package> --prefer-binary --find-links https://ext.kmtea.eu/wheels.html
```

If you have trouble accessing GitHub Pages,
you may try the CDN hosted by CloudFlare:

```bash
pip install <package> --prefer-binary --extra-index-url https://ext.kmtea.eu/cdn
```

```bash
pip install <package> --prefer-binary --find-links https://ext.kmtea.eu/wheels-cdn.html
```

## Others

### Source

This project contains wheels from:

* [pypy-wheels](https://github.com/KumaTea/pypy-wheels)
* [riscv-wheels](https://github.com/KumaTea/riscv-wheels)
* [musl-wheels](https://github.com/KumaTea/musl-wheels)

### Routine

I currently don't have a routine to build wheels,
instead I build them when needed.

If you would like a package to be built,
please open an issue.

### manylinux

`riscv64` is now supported by `manylinux`.
Since 2024-09 on linux only `manylinux`able wheels will be provided. 
