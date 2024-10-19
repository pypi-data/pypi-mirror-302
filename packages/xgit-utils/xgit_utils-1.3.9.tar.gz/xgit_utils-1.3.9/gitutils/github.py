import os
from typing import List

import click
from github import Auth, Github


def init_github(token: str = None) -> Github:
    if token is None:
        token = os.getenv('GITHUB_TOKEN')
        if token is None:
            raise ValueError(
                "A GitHub token must be provided either as a parameter or in the 'GITHUB_TOKEN' environment variable.")

    return Github(auth=Auth.Token(token=token))


def get_starred(token: str = None) -> List[str]:
    github = init_github(token)
    try:
        return [repo.clone_url for repo in github.get_user().get_starred()]
    finally:
        github.close()


def get_repos(token: str = None) -> List[str]:
    github = init_github(token)
    try:
        return [repo.clone_url for repo in github.get_user().get_repos()]
    finally:
        github.close()


def output_repos(output_file, repos):
    if output_file:
        with open(output_file, 'w') as file:
            for repo in repos:
                file.write(repo + '\n')
        click.echo(f"Repositories[{len(repos)}] have been written to {output_file}.")
    else:
        click.echo(f"Repositories[{len(repos)}]:")
        for repo in repos:
            click.echo(repo)


@click.command()
@click.option('-t', '--token', default=None, help='GitHub personal access token.')
@click.option('--mine', is_flag=True, help='Show user repositories.')
@click.option('-o', '--output-file', default=None, type=click.Path(), help='Output file to save the repositories.')
def execute(token, mine, output_file):
    try:
        click.echo("Running")
        if mine:
            repos = get_repos(token)
        else:
            repos = get_starred(token)
        output_repos(output_file, repos)
    except ValueError as e:
        click.echo(f"Error: {e}", err=True)
    except Exception as e:
        click.echo(f"An unexpected error occurred: {e}", err=True)


if __name__ == "__main__":
    execute()
