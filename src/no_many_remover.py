from col_whl import *


def is_bad_asset(name: str):
    return (
        name.endswith('.whl') and
        'linux' in name and
        (
            'manylinux' not in name and
            'musllinux' not in name
        )
    )


def del_bad_assets():
    releases = [f for f in os.listdir(f'{WORKDIR}\\whl\\data') if '_' in f]

    for release in releases:
        repo = release.split('_')[0]
        tag = release.split('_')[1].replace('.json', '')

        with open(f'{WORKDIR}\\whl\\data\\{release}', 'r', encoding='utf-8') as json_file:
            assets = json.load(json_file)

        print(f'\nChecking {repo} {tag}\n')
        pbar = tqdm(assets)
        for asset in pbar:
            name = asset['name']
            if is_bad_asset(name):
                # delete bad asset using gh
                pbar.set_description(f'  Deleting {name}')
                subprocess.run(
                    f'gh release delete-asset --repo KumaTea/{repo} {tag} {name} -y',
                    shell=True
                )


if __name__ == '__main__':
    if input('update? (Y/n) ').lower() != 'n':
        get_all_repo_data()
    del_bad_assets()
