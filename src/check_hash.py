import sys
import requests
from tools import *
from typing import Optional
# from rich.progress import Progress, TaskID


saved_hash = get_saved_hash()
saved_hash_whl = set(saved_hash.keys())
pkgs = get_assets_from_html()
pkg_urls = {pkg['name']: pkg['url'] for pkg in pkgs}
pkg_names = set(pkg_urls.keys())


def get_pkg_hash(
        filename: str,
        pbar: tqdm,
        # progress: Progress, task: TaskID
) -> tuple[Optional[str], bool]:
    """
    sha256sum, verified
    """
    if filename in saved_hash_whl:
        return saved_hash[filename]['sha256'], saved_hash[filename]['verify']

    # pkg_url = pkg_urls.get(filename)
    # if not pkg_url:
    #     return None, False
    # do an assertion
    pkg_url = pkg_urls[filename]
    pkg_url_split = pkg_url.split('#sha256=')
    if len(pkg_url_split) != 2:
        return None, False

    saved_hash[filename] = {'sha256': pkg_url_split[1], 'verify': False}
    pbar.set_description(f'{filename[:32]:<32} added to saved_hash')
    # progress.update(task, description=f'{filename[:32]:<32} added to saved_hash')
    return pkg_url_split[1], False


# https://gist.github.com/yanqd0/c13ed29e29432e3cf3e7c38467f42f51
def download(
        url: str,
        # progress: Progress
) -> bytes:
    r = requests.get(url, stream=True)
    content = b''
    total = int(r.headers.get('content-length', 0))

    # dl_task = progress.add_task(
    #     '\tDownloading...',
    #     total=total
    # )

    with tqdm(
        desc='  DL: ' + '{:<32}'.format(url.split('/')[-1].split('#')[0][:32]),
        total=total,
        unit='iB',
        unit_scale=True,
        unit_divisor=1024,
        file=sys.stdout,
    ) as bar:
        for data in r.iter_content(chunk_size=1024 * 64):
            content += data
            size = len(data)
            # progress.update(dl_task, advance=size)
            bar.update(size)
            # bar.refresh()
    # progress.update(dl_task, completed=True)
    # progress.remove_task(dl_task)
    return content


def check_remote_hash(
        url: str,
        # progress: Progress
):
    # cdn_url = f'https://gh.kmtea.eu/{url}'
    # r = requests.get(cdn_url)
    # assert r.status_code == 200, f'{cdn_url} failed ({r.status_code})!'
    # sha256_digest = hashlib.sha256(r.content).hexdigest()
    # sha256_digest = hashlib.sha256(download(cdn_url)).hexdigest()
    sha256_digest = hashlib.sha256(download(url)).hexdigest()
    # sha256_digest = hashlib.sha256(download(cdn_url, progress)).hexdigest()
    return sha256_digest


def main():
    print('\nChecking sha256sum...\n')

    pbar = tqdm(pkg_names, file=sys.stdout)
    # with Progress() as progress:
    # progress = Progress()
    # progress.start()

    # main_task = progress.add_task('Checking sha256sum...', total=len(pkg_names))
    i = 0
    # for pkg in pkg_names:
    for pkg in pbar:
        pbar.set_description(f'Now: {pkg[:48]:<48}')
        # progress.update(main_task, description=f'Now: {pkg[:48]:<48}')

        # pkg_sha256, pkg_verified = get_pkg_hash(pkg, progress, main_task)
        pkg_sha256, pkg_verified = get_pkg_hash(pkg, pbar)
        if pkg_verified:
            # progress.update(main_task, advance=1)
            continue

        # remote_sha256 = check_remote_hash(pkg_urls[pkg], progress)
        remote_sha256 = check_remote_hash(pkg_urls[pkg])
        if pkg_sha256:
            # has hash in url, verify it
            if pkg_sha256 == remote_sha256:
                pbar.set_description(f'{pkg[:48]:<48} verified!')
                # progress.update(main_task, description=f'{pkg[:48]:<48} verified!')
            else:
                msg = f'\n{pkg[:48]:<48} sha256sum not match!!!\n'
                pbar.write(msg)
                pbar.set_description(msg)
                # progress.update(main_task, description=msg)
                saved_hash[pkg]['sha256'] = remote_sha256
        else:
            # no hash in url
            saved_hash[pkg] = {
                'sha256': remote_sha256
            }
            msg = f'  {pkg[:48]:<48} added to saved_hash'
            # pbar.write(msg)
            pbar.set_description(msg)
            # progress.update(main_task, description=msg)

        # progress.update(main_task, advance=1)
        saved_hash[pkg]['verify'] = True

        # if pbar.n % 100 == 0:
        # may be skipped
        i += 1
        if i % 2 == 0:
            # print(f'Saving hash at {i}.')
            pbar.write(f'\nSaving hash at {pbar.n}.\n')
            save_hash(saved_hash)
        else:
            pbar.set_description(f'{2 - i % 2} left to save hash')

    # progress.stop()
    return saved_hash


if __name__ == '__main__':
    save_hash(main())
