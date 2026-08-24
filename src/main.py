from gen_whl import gen_html
from col_whl import get_all_repo_data
from check_hash import check as check_whl_hash
from tools import (get_saved_hash, get_assets, update_hash_dict, get_local_whl,
                   save_hash, backup_hashfile, bootstrap_hash_from_html)


if __name__ == '__main__':
    # for manually update:
    # repo = 'ext-whl'
    # tags = get_repo_release_tags('ext-whl')
    # tag = tags[0]
    # assets = get_release_assets(repo, tag)
    # save_release_data(repo, tag, assets)

    get_all_repo_data()

    backup_hashfile()
    hash_dict = get_saved_hash()
    if not hash_dict:
        # whl/data is gitignored, so a fresh clone starts empty. Recover the
        # hashes from the ones already embedded in wheels.html rather than
        # blanking them and re-downloading the entire index.
        print('No saved hashes found, bootstrapping from wheels.html...')
        hash_dict = bootstrap_hash_from_html()
        print(f'Recovered {len(hash_dict)} hashes.')

    wheels = get_assets(hash_dict)

    local_whl = get_local_whl()
    hash_dict = update_hash_dict(saved_hash=hash_dict, whl_files=local_whl, upl_whl=wheels)
    save_hash(hash_dict)

    # first pass: needed so check_whl_hash() sees the newly released wheels
    gen_html(hash_dict)
    # gen_index(wheels)

    hash_dict = check_whl_hash(hash_dict)
    save_hash(hash_dict)

    # second pass: wheels hashed just now had no #sha256= in the first pass
    gen_html(hash_dict)
