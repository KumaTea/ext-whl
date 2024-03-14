import shutil
import logging
from conf import *
from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from tools import get_assets, get_saved_hash, get_assets_from_html


whl_path = f'{WORKDIR}/whl/wheels.html'
index_dir = f'{WORKDIR}/whl/simple'
cdn_index_dir = f'{WORKDIR}/whl/cdn'
# PYPI_INDEX = 'https://pypi.org/simple'
# official index is too smart that it redirects underscore to dash
PYPI_INDEX = 'https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple'

check_counter = 0


def check_official(pkg_name: str) -> bool:
    official_index_url = f'{PYPI_INDEX}/{pkg_name}/'
    try:
        with urlopen(official_index_url) as response:
            is_200 = response.getcode() == 200
        if is_200:
            global check_counter
            check_counter += 1
            if check_counter % 100 == 0:
                print(f'Checked {check_counter} packages...')
            return True
        else:
            logging.warning(f'Package {pkg_name} not found ({response.getcode()}) on official PyPI!!!')
            return False
    except (HTTPError, URLError):
        logging.warning(f'Package {pkg_name} not found on official PyPI!!!')
        return False


def gen_index(assets: list):
    pkgs = {}

    for asset in assets:
        filename = asset['name']
        url = asset['url']
        pkg_name = filename.split('-')[0]

        # process package name
        pkg_name = pkg_name.replace('_', '-')
        pkg_name = pkg_name.replace('.', '-')
        pkg_name = pkg_name.lower()
        pkg_html = f'<a href="{url}">{filename}</a>'

        pkgs[pkg_name] = pkgs.get(pkg_name, []) + [(filename, pkg_html)]

    pkgs = {k: v for k, v in sorted(pkgs.items(), key=lambda item: item[0])}
    for pkg in pkgs:
        # check_official(pkg)
        pkgs[pkg].sort(key=lambda x: x[0])
        os.makedirs(f'{index_dir}/{pkg}', exist_ok=True)
        with open(f'{index_dir}/{pkg}/index.html', 'w', encoding='utf-8') as f:
            f.write(
                f'<!DOCTYPE html>\n'
                f'<html>\n'
                f'<head>\n'
                f'<meta name="pypi:repository-version" content="1.0">\n'
                f'<title>Links for {pkg}</title>\n'
                f'</head>\n'
                f'<body>\n'
                f'<h1>Links for {pkg}</h1>\n'
            )
            for pkg_filename, line in pkgs[pkg]:
                f.write(line + '<br>\n')
            f.write('</body></html>')

    with open(f'{index_dir}/index.html', 'w', encoding='utf-8') as f:
        f.write(
            '<!DOCTYPE html>\n'
            '<html>\n'
            '<head>\n'
            '<meta name="pypi:repository-version" content="1.0">\n'
            '<title>Package Index</title>\n'
            '<body>\n'
            '<h1>Package Index</h1>\n'
        )
        for pkg in pkgs:
            f.write(f'<a href="{pkg}">{pkg}</a><br>\n')
        f.write('</body></html>')

    return pkgs


def gen_cdn_index():
    shutil.copytree(index_dir, cdn_index_dir)
    files = os.walk(cdn_index_dir)
    for root, dirs, files in files:
        for file in files:
            if file.endswith('.html'):
                with open(f'{root}/{file}', 'r', encoding='utf-8') as f:
                    html = f.read()
                html = html.replace('https://github.com/', 'https://gh.kmtea.eu/https://github.com/')
                with open(f'{root}/{file}', 'w', encoding='utf-8') as f:
                    f.write(html)


if __name__ == '__main__':
    if os.name == 'nt':
        hash_dict = get_saved_hash()
        wheels = get_assets(hash_dict)
        if input('Check official index? ([Y]/n) ').lower() in ['', 'y']:
            from tqdm import tqdm
            for p in tqdm(gen_index(wheels)):
                check_official(p)
    else:
        wheels = get_assets_from_html()
        gen_index(wheels)
        gen_cdn_index()
