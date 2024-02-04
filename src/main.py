from gen_whl import gen_html
from gen_index import gen_index
from col_whl import get_all_repo_data
from tools import get_saved_hash, get_assets


if __name__ == '__main__':
    get_all_repo_data()

    hash_dict = get_saved_hash()
    wheels = get_assets(hash_dict)

    gen_html(hash_dict)
    gen_index(wheels)
