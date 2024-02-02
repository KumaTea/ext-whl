# ext-whl
Extended Python wheels (whl)

This project provides pre-built wheels of popular packages.

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

This project contains wheels from:

* [pypy-wheels](https://github.com/KumaTea/pypy-wheels)
* [riscv-wheels](https://github.com/KumaTea/riscv-wheels)
