import shutil as su
from pathlib import Path

from pydantic import DirectoryPath
from pydantic.dataclasses import dataclass
from jinja2 import Template

from .config import settings


_alembic_base: str = "alembic"
_static_base: str = "static"
_locales_base: str = "locales"
_templates_base: str = "templates"
_email_templates_base: str = "email_templates"

_templates_root: DirectoryPath = Path(__file__).parent.joinpath("templates")
_alembic_ini_filename: str = "alembic.ini"


def make_root_dir(path: Path | None = None) -> DirectoryPath:
    if path is None:
        path = settings.config_root
    path.mkdir(mode=0o755, parents=True, exist_ok=True)
    return path


def make_alembic_dir(path: Path | None = None) -> DirectoryPath:
    if path is None:
        path = settings.config_root / _alembic_base
    if path.exists():
        return path
    path.mkdir(mode=0o755, parents=True, exist_ok=True)

    # write alembic.ini
    template_file = _templates_root.joinpath("alembic", "alembic.ini")
    with open(template_file, 'r') as f:
        template = f.read()

    data = {
        'alembic_root': str(path),
        'database_dsn': settings.get_database_connection_parameters(asyncio=False)
    }
    ini = Template(template).render(data)

    ini_file = path.joinpath(_alembic_ini_filename)
    with open(ini_file, 'w') as f:
        f.write(ini)

    # copy all migrations
    src = _templates_root.joinpath("alembic", "migrations")
    dst = path.joinpath("migrations")
    su.copytree(src, dst, dirs_exist_ok=True)
    return path


def make_static_dir(path: Path | None = None) -> DirectoryPath:
    if path is None:
        path = settings.config_root / _static_base
    if path.exists():
        return path
    path.mkdir(mode=0o755, parents=True, exist_ok=True)

    src = _templates_root.joinpath("static")
    dst = path
    if src.exists():
        su.copytree(src, dst, dirs_exist_ok=True)
    return path


def make_locales_dir(path: Path | None = None) -> DirectoryPath:
    if path is None:
        path = settings.config_root / _locales_base
    if path.exists():
        return path
    path.mkdir(mode=0o755, parents=True, exist_ok=True)

    src = _templates_root.joinpath("locales")
    dst = path
    if src.exists():
        su.copytree(src, dst, dirs_exist_ok=True)
    return path


def make_templates_dir(path: Path | None = None) -> DirectoryPath:
    if path is None:
        path = settings.config_root / _templates_base
    if path.exists():
        return path
    path.mkdir(mode=0o755, parents=True, exist_ok=True)

    src = _templates_root.joinpath("templates")
    dst = path
    if src.exists():
        su.copytree(src, dst, dirs_exist_ok=True)
    return path


def make_email_templates_dir(path: Path | None = None) -> DirectoryPath:
    if path is None:
        path = settings.config_root / _email_templates_base
    if path.exists():
        return path
    path.mkdir(mode=0o755, parents=True, exist_ok=True)

    src = _templates_root.joinpath("email_templates")
    dst = path
    if src.exists():
        su.copytree(src, dst, dirs_exist_ok=True)
    return path


@dataclass
class PathSettings:
    root_dir: DirectoryPath = make_root_dir()
    alembic_dir: DirectoryPath = make_alembic_dir()
    static_dir: DirectoryPath = make_static_dir()
    locales_dir: DirectoryPath = make_locales_dir()
    templates_dir: DirectoryPath = make_templates_dir()
    email_templates_dir: DirectoryPath = make_email_templates_dir()

    @property
    def alembic_ini_file(self):
        return self.alembic_dir / _alembic_ini_filename


paths = PathSettings()
