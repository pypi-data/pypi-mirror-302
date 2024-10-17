import nox


@nox.session(venv_backend="uv")
def uv_init(session):
    session.install("uv")
    session.run("uv", "init", "D:\\Repos\\Test")
