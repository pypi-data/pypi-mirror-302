#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
"""
git clone tools
"""
import argparse
import os
import sys

import gitutils
from gitutils import utils


def run_clone(target_dir: str, repo: gitutils.GitRepo, prefix: str):
    utils.my_print(f">> {utils.Color.green(prefix)} begin to clone {utils.Color.red(repo.name)} from {repo.url}")

    cmd_clone_mirror = f"git clone --mirror {repo.url}"

    group_path = os.path.join(target_dir, repo.group)
    os.makedirs(group_path, exist_ok=True)

    repo_path = os.path.join(group_path, f"{repo.name}.git")

    if os.path.exists(repo_path):
        utils.my_print_red(">> Repo already exists")
        return

    os.chdir(group_path)
    os.system(cmd_clone_mirror)


def repo_clone(target_dir: str, url_file: str, ignore: bool = False):
    repo_list: list[str] = []
    ignore_list: list[str] = []

    if not os.path.exists(gitutils.XGIT):
        os.makedirs(gitutils.XGIT)

    if os.path.exists(gitutils.XGIT_IGNORE):
        with open(gitutils.XGIT_IGNORE, 'r') as f:
            lines = f.readlines()
            if lines and len(lines) > 0:
                for line in lines:
                    ignore_list.append(line.strip())

    if url_file.startswith("http") or url_file.startswith("git"):
        repo_list.append(url_file.strip())
    else:
        url_file = utils.abs_path(url_file.strip())
        if os.path.exists(url_file) and os.path.isfile(url_file):
            with open(url_file, 'r') as f:
                lines = f.readlines()
                if lines and len(lines) > 0:
                    for line in lines:
                        repo_list.append(line.strip())

    if ignore:
        for repo in repo_list:
            if not (repo.rstrip('/') in ignore_list):
                ignore_list.append(repo.rstrip("/"))
        with open(gitutils.XGIT_IGNORE, 'w') as f:
            f.writelines([line + '\n' for line in ignore_list])
        utils.my_print_green("Done")
        return

    filter_list: list[gitutils.GitRepo] = [gitutils.parse_git_url(item) for item in repo_list if
                                           not any(url in item for url in ignore_list)]
    filter_list = [item for item in filter_list if
                   not os.path.exists(os.path.join(target_dir, item.group, f"{item.name}.git"))]
    size: int = len(filter_list)
    if size > 0:
        for index, repo in enumerate(filter_list):
            run_clone(target_dir, repo, prefix="[{0}/{1}]".format(index + 1, size))
        utils.my_print_green(message="Done")
    else:
        utils.my_print_red(message="Exist")


def cmd_clone(args):
    try:
        gitutils.set_proxy(args=args)
        repo_clone(target_dir=args.target_dir, url_file=args.url_file, ignore=args.ignore)
    except Exception as e:
        utils.my_print_red(f"{e}")
    except KeyboardInterrupt:
        utils.my_print_red("Cancel")


def execute():
    """execute point
    :return:
    """
    if len(sys.argv) == 1:
        sys.argv.append('--help')
    parser = argparse.ArgumentParser(description=f'git clone {gitutils.__version__}', epilog='make it easy')
    parser.add_argument('--ignore',
                        help='Ignore repo', action='store_true', default=False)
    parser.add_argument('--target_dir', type=str,
                        help=u'Clone the Repo to the directory【default:{0}】'.format(gitutils.DEFAULT_GITHUB),
                        default=gitutils.DEFAULT_GITHUB)
    parser.add_argument("url_file", type=str, help=u'git URL or File')
    gitutils.parser_proxy(parser=parser)
    parser.set_defaults(func=cmd_clone)
    # parser args
    args = parser.parse_args()
    args.func(args)


def test():
    """
    test
    :return:
    """
    # sys.argv.append("--ignore")
    sys.argv.append("--target_dir")
    sys.argv.append("/Users/seven/Mirror/github")
    sys.argv.append("~/Desktop/git.txt")
    # sys.argv.append("https://github.com/hcengineering/platform/")


if __name__ == '__main__':
    test()
    execute()
