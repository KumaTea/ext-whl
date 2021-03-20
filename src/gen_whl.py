import requests
from urllib.parse import quote_plus


author = 'KumaTea'
project = 'ext-whl'
whl_dir = '../whl'
whl_file = 'stable.html'
gh_rl_api = 'https://api.github.com/repos/{author}/{project}/releases'


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


if __name__ == '__main__':
    html = gen_index()
    with open(f'{whl_dir}/{whl_file}', 'w', encoding='utf-8') as html_file:
        html_file.write(html)
