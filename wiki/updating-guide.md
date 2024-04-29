# Guide To Keep Full Application Updated

## Update Python For Backend App

- Download and install latest python version
- Update python version in src/pyproject.toml
- Delete and recreate new virtual environment with poetry with newly installed python version
- Update vscode python used for project
- Update Python version in following files:
  - .github/workflows/lint-check.yml
  - .github/workflows/run-tests-no-docker.yml
  - src/Dockerfile
  - src/Dockerfile.web
  - src/playwright.Dockerfile
- Run all tests and update code if required

## Update Poetry

Poetry should be installed globally with pipx

- Run `pipx upgrade poetry`

## Update Python Packages for backend app

- To update any package to the latest version, run: `poetry add package-name@latest`
- Run all tests and update code if required

## Update Docker-Compose File Version

- Update 1st line in docker-compose to latest version
- Make any required changes

## Docker-based Databases

Currently MySql, Mongo & Redis build the latest images.
Once we fix the version, update will need to be done regularly following:

- Upgrade docker image of db to latest version
- Run all tests and update code if required
