[![Release](https://img.shields.io/github/v/release/zawadzkim/cookiecutter-hydro)](https://pypi.org/project/cookiecutter-hydro/)
[![Build status](https://img.shields.io/github/actions/workflow/status/zawadzkim/cookiecutter-hydro/main.yml?branch=main)](https://github.com/zawadzkim/cookiecutter-hydro/actions/workflows/main.yml?query=branch%3Amain)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/cookiecutter-hydro)](https://pypi.org/project/cookiecutter-hydro/)
[![Docs](https://img.shields.io/badge/docs-gh--pages-blue)](https://zawadzkim.github.io/cookiecutter-hydro/)
[![License](https://img.shields.io/github/license/zawadzkim/cookiecutter-hydro)](https://img.shields.io/github/license/zawadzkim/cookiecutter-hydro)

## Main features

- [Poetry](https://python-poetry.org/) for dependency management
- [GitHub Actions](https://github.com/features/actions)
- Pre-commit hooks with [pre-commit](https://pre-commit.com/)
- Code quality with [ruff](https://github.com/charliermarsh/ruff), [mypy](https://mypy.readthedocs.io/en/stable/), [deptry](https://github.com/zawadzkim/deptry/) and [prettier](https://prettier.io/)
- Containerization with [Docker](https://www.docker.com/)
- Development environment with [VSCode devcontainers](https://code.visualstudio.com/docs/devcontainers/containers)

## Quickstart

On your local machine, navigate to the directory in which you want to
create a project directory, and run the following two commands:

```bash
pip install cookiecutter-hydro
cchydro
```

Alternatively, install `cookiecutter` and directly pass the URL to this
Github repository to the `cookiecutter` command:

```bash
pip install cookiecutter
cookiecutter https://github.com/zawadzkim/cookiecutter-hydro.git
```

Create a repository on GitHub, and then run the following commands, replacing `<project-name>`, with the name that you gave the Github repository and
`<github_author_handle>` with your Github username.

```bash
cd <project_name>
git init -b main
git add .
git commit -m "Init commit"
git remote add origin git@github.com:<github_author_handle>/<project_name>.git
git push -u origin main
```

Finally, install the environment and the pre-commit hooks with

```bash
make install
```

You are now ready to start development on your project!

## Acknowledgements

This project is a fork of [Cookiecutter Poetry](https://github.com/zawadzkim/cookiecutter-hydro-example) and is partly inspired by [Cookiecutter Data Science](https://github.com/drivendataorg/cookiecutter-data-science) project, but is tailored for use in hydrological research.
