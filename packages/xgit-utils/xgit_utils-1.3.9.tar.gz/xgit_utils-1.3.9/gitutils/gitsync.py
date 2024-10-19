#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
"""
git sync tools
"""

import argparse
import os
import sys
import time
from multiprocessing import Pool

from tqdm import tqdm

import gitutils
from gitutils import utils


def repos_fetch(target_dir: str, repo_list: list[gitutils.Repo], thread_size: int):
    if thread_size <= 0:
        thread_size = 1
    pool = Pool(processes=thread_size)
    size = len(repo_list)
    for index, repo in enumerate(repo_list):
        pool.apply_async(repo_fetch, args=(repo.path, target_dir, size, index))
    pool.close()
    pool.join()


def repo_fetch(repo: str, target_dir: str, size: int, index: int):
    utils.my_print('[{0}/{1}] - {2}'.format(index + 1,
                                            size, repo.replace(target_dir, '')))
    gitutils.exec_fetch(repo_dir=repo)


def repo_sync(target_dir: str,
              thread_size: int,
              filter_host: list[str] = None,
              list_remote: bool = False,
              list_repo: bool = False,
              repo: str = None,
              notify: bool = False,
              export: bool = False):
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    """:type:str"""
    start_time = time.time()
    utils.my_print('>> Start: {0}'.format(time.strftime(
        '%Y-%m-%d %H:%M:%S', time.localtime(start_time))))

    repo_list = gitutils.scan_repo(root_dir=target_dir,
                                   filter_host=filter_host)
    if list_remote:
        if not repo_list:
            utils.my_print_red('>> no repo')
            return

        remote_list: list[str] = []

        for repo in repo_list:
            if not (repo.host in remote_list):
                remote_list.append(repo.host)

        size = len(remote_list)
        for index, host in enumerate(remote_list):
            utils.my_print('[{0}/{1}] - {2}'.format(index + 1, size, host))

    elif list_repo:
        if not repo_list:
            utils.my_print_red('>> no repo')
            return

        folder_list = []

        for repo in tqdm(repo_list, desc="Processing", unit="items"):
            folder_list.append(utils.folder_size(repo.path, repo.url))

        folder_list.sort(key=lambda f: f.size)

        size = len(repo_list)
        for index, folder in enumerate(folder_list):
            utils.my_print('[{0}/{1}] - {2} - {3}'.format(index + 1, size, folder.mess, folder.url))

    elif export:
        if not repo_list:
            utils.my_print_red('>> no repo')
            return

        size = len(repo_list)
        export_content = '\n'.join([repo.url for repo in repo_list])

        current_time = time.strftime('%Y%m%d%H%M%S')
        export_file = os.path.join(os.getcwd(), f'repo-{current_time}.txt')

        with open(export_file, 'w') as f:
            f.write(export_content.strip())

        utils.my_print_green(f'export [{size}] repo - {export_file}')

    elif repo:
        repos: list[gitutils.Repo] = []
        t_list = [x for x in repo.split(",") if x != ""]
        for x in repo_list:
            for y in t_list:
                if x.url.lower().find(y.lower()) > -1:
                    repos.append(x)
                    break
        repos_fetch(target_dir=target_dir, repo_list=repo_list, thread_size=thread_size)
    else:
        repos_fetch(target_dir=target_dir, repo_list=repo_list, thread_size=thread_size)
    end_time = time.time()
    utils.my_print('>> End {0}'.format(time.strftime(
        '%Y-%m-%d %H:%M:%S', time.localtime(end_time))))
    run_time = int(end_time - start_time)
    utils.my_print('>> Time: {0}'.format(utils.time_count(run_time)))
    if notify:
        utils.notify(content="Done", title="GitSync")


def cmd_sync(args):
    """git sync
    :param args:
    :return:
    """
    try:
        gitutils.set_proxy(args=args)
        repo_sync(target_dir=args.target_dir,
                  thread_size=args.thread,
                  filter_host=args.filter_host,
                  list_remote=args.list_remote,
                  list_repo=args.list_repo,
                  repo=args.repo,
                  notify=args.notify,
                  export=args.export)
    except Exception as e:
        utils.my_print_red(f"{e}")
    except KeyboardInterrupt:
        utils.my_print_red("Cancel")


def config_args(parser):
    """
    set args
    :param parser:
    :return:
    """
    parser.add_argument('-d', '--target_dir', type=str, default=gitutils.DEFAULT_GITHUB,
                        help='target dir【default:{0}】'.format(gitutils.DEFAULT_GITHUB))
    parser.add_argument('-t', '--thread', type=int, default=gitutils.DEFAULT_THREAD_SIZE,
                        help="number of threads 【default:{0}】".format(gitutils.DEFAULT_THREAD_SIZE))
    parser.add_argument('-f', '--filter_host',
                        action='append', help='filter host')
    # sync repo
    parser.add_argument('-r', '--repo', type=str,
                        help="sync repo - [okhttp,ffmpeg,...]")
    # show remote list
    parser.add_argument('--list_remote',
                        help='show remote list', action='store_true', default=False)
    # show repo list
    parser.add_argument('--list_repo', action='store_true', default=False, help='show repo list')
    # show notify
    parser.add_argument('--notify', action='store_true', default=False, help='show notify')
    parser.add_argument('--export', action='store_true', default=False, help='export repos')
    gitutils.parser_proxy(parser=parser)
    parser.set_defaults(func=cmd_sync)


def execute():
    """execute point
    :return:
    """
    parser = argparse.ArgumentParser(
        description=f'git sync {gitutils.__version__}', epilog='make it easy')
    config_args(parser)
    # parser args
    args = parser.parse_args()
    args.func(args)


def test():
    sys.argv.append('-d')
    sys.argv.append('/Users/seven/mirror')

    sys.argv.append('-t')
    sys.argv.append('10')

    sys.argv.append('-f')
    sys.argv.append('github.com')

    sys.argv.append('--list_repo')


if __name__ == '__main__':
    test()
    execute()
