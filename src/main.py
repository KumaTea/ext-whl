from gen_index import gen_index
from col_whl import get_all_repo_data
from tools import get_saved_hash, get_assets, trim_hash_dict
from gen_whl import gen_html, get_local_whl, extend_hash_dict, save_hash


if __name__ == '__main__':
    get_all_repo_data()

    hash_dict = get_saved_hash()
    wheels = get_assets(hash_dict)

    local_whl = get_local_whl()
    hash_dict = extend_hash_dict(hash_dict, local_whl)

    hash_dict = trim_hash_dict(wheels, hash_dict)
    save_hash(hash_dict)

    gen_html(hash_dict)
    # gen_index(wheels)
