from gen_whl import gen_html
from col_whl import get_all_repo_data
from check_hash import check as check_whl_hash
from tools import get_saved_hash, get_assets, update_hash_dict, get_local_whl, save_hash, backup_hashfile


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
    wheels = get_assets(hash_dict)

    local_whl = get_local_whl()
    hash_dict = update_hash_dict(saved_hash=hash_dict, whl_files=local_whl, upl_whl=wheels)
    save_hash(hash_dict)

    gen_html(hash_dict)
    # gen_index(wheels)

    # don't forget to run check_hash.py
    new_hash_dict = check_whl_hash(hash_dict)
    save_hash(new_hash_dict)
