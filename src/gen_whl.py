import requests
from urllib.parse import quote_plus


author = 'KumaTea'
project = 'ext-whl'
whl_dir = '../whl'
whl_file = 'stable.html'
dev_file = 'dev.html'
gh_rl_api = 'https://api.github.com/repos/{author}/{project}/releases'

dev_packages = {
    'numpy': {
        'ver': ['1.20'],
        'py': 'cp36'
    },
    'h5py': {
        'ver': ['3.2'],
        'py': 'cp36'
    }
}


def get_gh_rl(author_name, project_name):
    print('Fetching GitHub releases...')
    assets = []
    result_raw = requests.get(gh_rl_api.format(author=author_name, project=project_name)).json()
    for release in result_raw:
        if release['assets']:
            for binary in release['assets']:
                if 'whl' in binary['name']:
                    assets.append({
                        'name': binary['name'],
                        'url': binary['browser_download_url']
                    })
    return assets


def gen_index():
    rl_list = get_gh_rl(author, project)
    rl_html = ''
    for file in rl_list:
        whl_index = '<a href=\"' + file['url'] + '\">' + quote_plus(file['name']) + '</a><br>\n'
        rl_html += whl_index
    return rl_html


def pick_dev():
    raw_html = gen_index()
    packages_list = raw_html.splitlines()
    dev_list = []
    for package in dev_packages:
        for item in packages_list:
            if package in item:
                for ver in dev_packages[package]['ver']:
                    if ver in item and dev_packages[package]['py'] in item:
                        dev_list.append(item)
                        packages_list.remove(item)
    stable_html = '\n'.join(packages_list) + '\n'
    dev_html = '\n'.join(dev_list) + '\n'
    return stable_html, dev_html


def gen_html():
    stable, dev = pick_dev()
    with open(f'{whl_dir}/{whl_file}', 'w', encoding='utf-8') as html_file:
        html_file.write(stable)
    with open(f'{whl_dir}/{dev_file}', 'w', encoding='utf-8') as html_file:
        html_file.write(dev)


def gen_html_cdn():
    with open(f'{whl_dir}/{whl_file}', 'r', encoding='utf-8') as html_file:
        html = html_file.read()
    with open(f'{whl_dir}/stable-cn.html', 'w', encoding='utf-8') as html_file:
        html_file.write(html.replace('https://github.com/', 'https://gh.kmtea.eu/https://github.com/'))
