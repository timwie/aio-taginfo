from invoke import task, Context

@task
def doc(c: Context):
    """Generate documentation"""
    c.run("pdoc -o ./doc aio_taginfo/", echo=True, pty=True)

@task
def doco(c: Context):
    """Generate documentation and open in browser"""
    from pathlib import Path
    import webbrowser

    doc(c)

    path = Path(__file__).parent / "doc" / "index.html"
    url = f"file://{path}"
    webbrowser.open(url, new=0, autoraise=True)

@task
def fmt(c: Context):
    """Run code formatters"""
    c.run("isort aio_taginfo/ tests/", echo=True, pty=True)
    c.run("black aio_taginfo/ tests/", echo=True, pty=True)

@task
def lint(c: Context):
    """Run linter and type checker"""
    c.run("ruff check aio_taginfo/", echo=True, warn=True, pty=True)
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
    c.run("poetry self update", echo=True, pty=True)
    c.run("poetry up --latest --only=dev", echo=True, pty=True)
    c.run("poetry show --outdated --why", echo=True, pty=True)
