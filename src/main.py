# from gen_index import gen_index
from gen_whl import gen_html
from col_whl import get_all_repo_data
from tools import get_saved_hash, get_assets, update_hash_dict, get_local_whl, save_hash


if __name__ == '__main__':
    get_all_repo_data()

    hash_dict = get_saved_hash()
    wheels = get_assets(hash_dict)

    local_whl = get_local_whl()
    hash_dict = update_hash_dict(saved_hash=hash_dict, whl_files=local_whl, upl_whl=wheels)
    save_hash(hash_dict)

    gen_html(hash_dict)
    # gen_index(wheels)

    # don't forget to run check_hash.py
