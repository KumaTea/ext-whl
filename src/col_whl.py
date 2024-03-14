import json
import subprocess
from conf import *
from tqdm import tqdm


def get_repo_release_tags(repo: str, author: str = AUTHOR) -> list:
    tags = []
    cmd = f'gh release list --repo {author}/{repo} --json tagName'
    raw_result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    result = json.loads(raw_result.stdout)
    for tag_dict in result:
        tags.append(tag_dict['tagName'])
    return tags


def get_release_assets(repo: str, tag: str, author: str = AUTHOR) -> list:
    cmd = f'gh release view --repo {author}/{repo} {tag} --json assets'
    raw_result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    result = json.loads(raw_result.stdout)
    return result['assets']


def save_release_data(repo: str, tag: str, data: list):
    with open(f'{WORKDIR}/whl/data/{repo}_{tag}.json', 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, indent=2)


def get_all_repo_data():
    os.makedirs(f'{WORKDIR}/whl/data', exist_ok=True)

    for repo in PROJECTS:
        print(f'\nFetching GitHub releases for {AUTHOR}/{repo}...')
        tags = get_repo_release_tags(repo)
        pbar = tqdm(tags)
        for tag in pbar:
            pbar.set_description(f'Fetching {tag:>8}...')
            assets = get_release_assets(repo, tag)
            save_release_data(repo, tag, assets)


if __name__ == '__main__':
    if input('Fetch all data? ([Y]/n) ') in ('', 'y', 'Y'):
        get_all_repo_data()
        print('Done.')
