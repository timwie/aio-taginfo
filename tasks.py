from invoke import Context, task


@task
def doc(c: Context):
    """Generate documentation"""
    c.run("pdoc -o ./doc aio_taginfo/", echo=True, pty=True)


@task
def doco(c: Context):
    """Generate documentation and open in browser"""
    import webbrowser
    from pathlib import Path

    doc(c)

    path = Path(__file__).parent / "doc" / "index.html"
    url = f"file://{path}"
    webbrowser.open(url, new=0, autoraise=True)


@task
def fmt(c: Context):
    """Run code formatters"""
    c.run("isort aio_taginfo/ tests/ tasks.py", echo=True, pty=True)
    c.run("ruff format aio_taginfo/ tests/ tasks.py", echo=True, pty=True)


@task
def install(c: Context):
    """Install all dependencies"""
    c.run("poetry lock --no-update", echo=True, pty=True)
    c.run("poetry install", echo=True, pty=True)


@task
def integration(c: Context):
    """Run integration tests"""
    c.run("python -m tests.v4.integration", echo=True, pty=True)


@task
def lint(c: Context):
    """Run linter and type checker"""
    c.run("ruff check aio_taginfo/ tests/", echo=True, warn=True, pty=True)
    c.run("mypy aio_taginfo/", echo=True, warn=True, pty=True)
    c.run("pyright aio_taginfo/", echo=True, warn=True, pty=True)


@task
def test(c: Context):
    """Run tests"""
    c.run("pytest -vv --cov=aio_taginfo/ --tb=native", echo=True, pty=True)


@task
def test_publish(c: Context):
    """Perform a dry run of publishing the package"""
    c.run("poetry publish --build --dry-run --no-interaction", echo=True, pty=True)


@task
def tree(c: Context):
    """Display the tree of dependencies"""
    c.run("poetry show --without=dev --tree", echo=True, pty=True)


@task
def update(c: Context):
    """Update dependencies"""
    c.run("poetry up --latest --only=dev", echo=True, pty=True)
    c.run("poetry show --outdated --why --with=dev", echo=True, pty=True)
