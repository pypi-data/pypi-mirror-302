# -*- coding: utf-8 -*-
"""
git utils
"""

import configparser
import os
import re
from dataclasses import dataclass
from typing import List
from urllib import parse

import gitutils.utils

__version__ = "1.3.9"

DEFAULT_PROXY = "127.0.0.1:1087"
DEFAULT_GITHUB = os.path.expanduser("~/Mirror/github")
XGIT = os.path.expanduser('~/.xgit')
XGIT_IGNORE = os.path.join(XGIT, '.xgitignore')
DEFAULT_THREAD_SIZE = 6


def parser_proxy(parser):
    """
    set proxy
    :param parser:
    :return:
    """
    # use proxy
    parser.add_argument('-u', '--use_proxy', help='use proxy', action='store_true', default=False)
    # proxy
    parser.add_argument('-p', '--proxy', help='http[s] proxy【default:{0}】'.format(DEFAULT_PROXY), type=str,
                        default=DEFAULT_PROXY)


def set_proxy(args):
    """
    set proxy
    :param args:
    :return:
    """
    try:
        use_proxy = args.use_proxy
        proxy = args.proxy
        if use_proxy and proxy:
            if utils.is_connected(url=proxy):
                os.environ.setdefault(key="http_proxy", value="http://{}".format(proxy))
                os.environ.setdefault(key="https_proxy", value="http://{}".format(proxy))
    except AttributeError:
        pass


def exec_fetch(repo_dir: str):
    os.chdir(repo_dir)
    os.system('git fetch origin')


@dataclass
class Repo:
    path: str
    url: str
    host: str


def parse_host(url: str) -> str:
    parsed_url = parse.urlparse(url) if url else None
    if parsed_url and parsed_url.hostname:
        return parsed_url.hostname

    ssh_pattern = r'^(?:git@)([^:]+):.*$'
    match = re.match(ssh_pattern, url)
    if match:
        return match.group(1)

    return ""


@dataclass
class GitRepo:
    url: str
    group: str
    name: str
    host: str


def parse_git_url(git_url: str) -> GitRepo:
    url = git_url
    if url.startswith("git@"):
        url = url.replace(":", "/").replace("git@", "https://")

    parse_result = parse.urlparse(url)
    hostname = parse_result.hostname.strip()

    parse_path = parse_result.path.rstrip("/")
    if parse_path.endswith(".git"):
        parse_path = parse_path[:-4]

    paths = [x for x in parse_path.split("/") if x]

    if len(paths) < 2:
        raise ValueError("The 'git URL' format is incorrect")

    group, name = paths[0], paths[1]

    if hostname == "github.com" and not url.endswith(".git"):
        url = url.rstrip("/") + ".git"

    if not git_url.startswith("git@"):
        git_url = url

    return GitRepo(url=git_url, group=group, host=hostname, name=name)


def parse_url(file_path: str) -> str:
    config = configparser.ConfigParser()
    config.read(file_path)
    try:
        return config['remote "origin"']['url']
    except KeyError:
        return ""


def scan_repo(root_dir: str, filter_host: list[str] = None) -> List[Repo]:
    if not os.path.isdir(root_dir):
        return []

    desired_dirs: List[Repo] = []

    for root, dirs, files in os.walk(root_dir):
        if '.git' in dirs or '.svn' in dirs:
            dirs[:] = []
            continue

        if 'refs' in dirs and 'objects' in dirs:
            conf_path = os.path.join(root, 'config')
            url = parse_url(conf_path) if os.path.isfile(conf_path) else ""
            host = parse_host(url)
            if filter_host and len(filter_host) > 0:
                if host in filter_host:
                    desired_dirs.append(Repo(path=root, url=url, host=host))
            else:
                desired_dirs.append(Repo(path=root, url=url, host=host))
            dirs[:] = []
        else:
            dirs[:] = [d for d in dirs if d not in {'refs', 'objects'}]

    return desired_dirs
