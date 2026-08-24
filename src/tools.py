import os
import json
import shutil
import hashlib
import logging
from conf import WORKDIR, LOCAL_WHL_DIR

try:
    from tqdm import tqdm
except ImportError:
    print('tqdm not found, fallback to normal list')
    tqdm = lambda x: x


def get_data_dir():
    data_dir = f'{WORKDIR}/whl/data'
    os.makedirs(data_dir, exist_ok=True)
    return data_dir


def get_saved_hash():
    file = f'{WORKDIR}/whl/data/sha256sums.json'
    if os.path.exists(file):
        with open(file, 'r', encoding='utf-8') as json_file:
            return json.load(json_file)
    return {}


def bootstrap_hash_from_html(verified: bool = True) -> dict:
    """
    Rebuild the hash dict from the sha256 fragments already in wheels.html.

    whl/data is gitignored, so a fresh clone has no sha256sums.json. Without
    this, update_hash_dict() would blank every hash and check_hash would then
    re-download the whole index to earn them back.

    Those fragments were written by add_sha256_to_url() from hashes an earlier
    run had already downloaded and verified, so they are treated as verified
    here too. Pass verified=False to force a full re-download instead.
    """
    saved_hash = {}
    for pkg in get_assets_from_html():
        url_split = pkg['url'].split('#sha256=')
        if len(url_split) == 2:
            saved_hash[pkg['name']] = {'sha256': url_split[1], 'verify': verified}
    return saved_hash


def backup_hashfile():
    hashfile = f'{get_data_dir()}/sha256sums.json'
    if not os.path.exists(hashfile):
        logging.warning('No sha256sums.json to back up (first run?), skipping.')
        return
    shutil.copyfile(hashfile, hashfile + '.bak')


def save_hash(saved_hash: dict):
    saved_hash = dict(sorted(saved_hash.items(), key=lambda x: x[0].lower()))
    with open(f'{get_data_dir()}/sha256sums.json', 'w', encoding='utf-8') as json_file:
        json.dump(saved_hash, json_file, indent=2)


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
    releases = [file for file in os.listdir(get_data_dir()) if file.endswith('json')]
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


def calculate_hash(file: str, algorithm: str = 'sha256') -> str:
    with open(file, 'rb') as f:
        hash_obj = hashlib.new(algorithm)
        hash_obj.update(f.read())
        return hash_obj.hexdigest()


def get_local_whl() -> list[tuple[str, str]]:
    """
    Get all .whl files in LOCAL_WHL_DIR
    :return: list of tuples (filename, path)
    """
    if not os.path.isdir(LOCAL_WHL_DIR):
        # not fatal: any wheel missing a hash here gets one from check_hash,
        # which downloads it from the release instead. Just don't do it silently.
        logging.warning(f'LOCAL_WHL_DIR {LOCAL_WHL_DIR} not found; '
                        f'hashes will be fetched from GitHub instead.')
        return []

    whl_files = []
    for root, dirs, files in os.walk(LOCAL_WHL_DIR):
        for file in files:
            if file.endswith('.whl'):
                whl_files.append((file, os.path.join(root, file)))
    return whl_files


def update_hash_dict(saved_hash: dict[str, dict], whl_files: list[tuple[str, str]], upl_whl: list[dict[str, str]]) -> dict:
    # saved_wheels = saved_hash.keys()
    # assert not any(name in saved_wheels for name, _ in whl_files), r'E:\Cache\whl is not empty!'

    new_saved_hash = {}
    for item in upl_whl:
        name = item['name']
        new_saved_hash[name] = {
            'sha256': saved_hash.get(name, {}).get('sha256', ''),
            'verify': saved_hash.get(name, {}).get('verify', False)
        }

    print('Calculating hash for local wheels...')
    for name, path in whl_files:
        if name in new_saved_hash:
            new_saved_hash[name]['sha256'] = calculate_hash(path)
            new_saved_hash[name]['verify'] = False

    return new_saved_hash


def remove_local_dup():
    saved_hash = get_saved_hash()
    local_whl = get_local_whl()

    for name, path in local_whl:
        if name in saved_hash:
            input(f'{name} already exists, remove?')
            os.remove(path)
