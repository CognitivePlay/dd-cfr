"""Configuration for nox."""

import tempfile

import nox
import nox_poetry

python_versions = ["3.9"]

nox.options.sessions = ("lint", "mypy", "safety", "formatter", "typeguard", "test")

locations = ["src", "tests", "noxfile.py"]
package = "dd_cfr"


@nox_poetry.session(python=python_versions)
def test(session):
    pytest_args = session.posargs or ["--cov"]
    session.run("poetry", "install", "--only", "main", external=True)
    session.install("coverage[toml]", "pytest", "pytest-cov")
    session.run("pytest", *pytest_args)


@nox_poetry.session(python=python_versions)
def lint(session):
    args = session.posargs or locations
    session.install(
        "flake8",
        "flake8-annotations",
        "flake8-bandit",
        "flake8-black",
        "flake8-bugbear",
        "flake8-import-order",
        "flake8-rst-docstrings",
        "darglint",
        "pylint",
    )
    session.run("flake8", *args)
    session.run("pylint", *args)


@nox_poetry.session(python=python_versions)
def mypy(session):
    args = session.posargs or locations
    session.install("mypy")
    session.run("mypy", *args)


@nox_poetry.session(python=python_versions)
def formatter(session):
    args = session.posargs or locations
    session.install(
        "black",
        "pydocstringformatter",
    )
    session.run("black", *args)
    session.run("pydocstringformatter", "--exit-code", *args)


@nox_poetry.session(python=python_versions)
def safety(session):
    with tempfile.TemporaryDirectory() as tmpdir:
        filename = tmpdir + "/reqs.txt"
        session.run(
            "poetry",
            "export",
            "--with",
            "dev",
            "--format=requirements.txt",
            "--without-hashes",
            f"--output={filename}",
            external=True,
        )
        session.install("safety")
        session.run("safety", "check", f"--file={filename}", "--full-report")


@nox_poetry.session(python=python_versions)
def typeguard(session):
    args = session.posargs or []
    session.run("poetry", "install", "--no-dev", external=True)
    session.install("pytest", "pytest-mock", "typeguard")
    session.run("pytest", f"--typeguard-packages={package}", *args)


@nox_poetry.session(python=python_versions)
def docs(session):
    session.run("poetry", "install", "--no-dev", external=True)
    session.install("sphinx", "sphinx-autodoc-typehints", "sphinx-rtd-theme")
    session.run("rm", "-rf", "docs/_build", "docs/_autosummary", external=True)
    session.run("sphinx-build", "-W", "docs", "docs/_build")
