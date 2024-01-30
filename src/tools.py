import json
import logging
from conf import *
from tqdm import tqdm


def get_saved_hash():
    file = f'{WORKDIR}/whl/data/sha256sums.json'
    if os.path.exists(file):
        with open(file, 'r', encoding='utf-8') as json_file:
            return json.load(json_file)
    return {}


def get_whl_sha256(name: str, saved_hash: dict):
    if name in saved_hash:
        return saved_hash[name]['sha256']
    return None


def add_sha256_to_url(name: str, url: str, saved_hash: dict):
    sha256sum = get_whl_sha256(name, saved_hash)
    if sha256sum:
        url += f'#sha256={sha256sum}'
    return url


def check_dup(assets: list):
    assets_dict = {}
    for asset in assets:
        assets_dict[asset['name']] = assets_dict.get(asset['name'], []) + [asset['url']]
    for name, urls in assets_dict.items():
        if len(urls) > 1:
            logging.warning(f'Duplicated assets: {name}')
            for url in urls:
                logging.warning(f'\tURL: {url}')


def get_assets(saved_hash: dict):
    assets = []
    releases = os.listdir(f'{WORKDIR}/whl/data')
    if 'sha256sums.json' in releases:
        releases.remove('sha256sums.json')

    for filename in tqdm(releases):
        with open(f'{WORKDIR}/whl/data/{filename}', 'r', encoding='utf-8') as json_file:
            release = json.load(json_file)
        for binary in release:
            if binary['name'].endswith('.whl'):
                assets.append({
                    'name': binary['name'],
                    'url': add_sha256_to_url(binary['name'], binary['url'], saved_hash)
                })
    return assets


def get_assets_from_html() -> list:
    pkgs = []
    whl_path = f'{WORKDIR}/whl/wheels.html'
    with open(whl_path, 'r', encoding='utf-8') as f:
        whl_html = f.read()

    for line in whl_html.split('\n'):
        if '<a' in line:
            a_tag_open_start = line.find('<a href="')
            a_tag_open_end = line.find('">')
            a_tag_close = line.find('</a>')
            pkg_filename = line[a_tag_open_end + len('">'):a_tag_close]
            pkg_url = line[a_tag_open_start + len('<a href="'):a_tag_open_end]
            pkgs.append({'name': pkg_filename, 'url': pkg_url})

    return pkgs
