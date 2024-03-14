from tools import *


def gen_html_content(saved_hash: dict):
    assets = get_assets(saved_hash)
    check_dup(assets)
    html = ''

    # sort by filename
    assets.sort(key=lambda x: x['name'].lower())

    for file in assets:
        whl_index = (
                '<a href=\"' + file['url'] + '\">' +
                file['name'] +
                '</a><br>\n')
        html += whl_index
    return ('<!DOCTYPE html>'
            '<html><body>\n'
            f'{html}'
            '</body></html>')


def gen_html(saved_hash: dict):
    index = gen_html_content(saved_hash)
    with open(f'{WORKDIR}/whl/wheels.html', 'w', encoding='utf-8') as html_file:
        html_file.write(index)


def gen_html_cdn():
    with open(f'{WORKDIR}/whl/wheels.html', 'r', encoding='utf-8') as html_file:
        html = html_file.read()
    with open(f'{WORKDIR}/whl/wheels-cdn.html', 'w', encoding='utf-8') as html_file:
        html_file.write(html.replace('https://github.com/', 'https://gh.kmtea.eu/https://github.com/'))


if __name__ == '__main__':
    if os.name == 'nt':
        hash_dict = get_saved_hash()
        local_whl = get_local_whl()
        hash_dict = extend_hash_dict(hash_dict, local_whl)
        save_hash(hash_dict)
        gen_html(hash_dict)
    else:
        gen_html_cdn()
