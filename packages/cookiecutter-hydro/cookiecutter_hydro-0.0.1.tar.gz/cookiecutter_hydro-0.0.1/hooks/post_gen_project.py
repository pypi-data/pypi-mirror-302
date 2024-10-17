#!/usr/bin/env python
from __future__ import annotations

import os
import shutil

PROJECT_DIRECTORY = os.path.realpath(os.path.curdir)


def remove_file(filepath: str) -> None:
    os.remove(os.path.join(PROJECT_DIRECTORY, filepath))


def remove_dir(filepath: str) -> None:
    shutil.rmtree(os.path.join(PROJECT_DIRECTORY, filepath))


if __name__ == "__main__":
    if "{{cookiecutter.include_github_actions}}" != "y":
        remove_dir(".github")

    if "{{cookiecutter.model}}" != "flopy":
        remove_dir("{{cookiecutter.project_slug}}/src/modflow")
        remove_dir("{{cookiecutter.project_slug}}/data/layers")
        remove_dir("{{cookiecutter.project_slug}}/data/boundaries")

    if "{{cookiecutter.model}}" != "swap":
        remove_dir("{{cookiecutter.project_slug}}/src/swap")

    if "{{cookiecutter.model}}" != "pastas":
        remove_dir("{{cookiecutter.project_slug}}/src/pastas")

    if "{{cookiecutter.dockerfile}}" != "y":
        remove_file("Dockerfile")

    if "{{cookiecutter.devcontainer}}" != "y":
        remove_dir(".devcontainer")
