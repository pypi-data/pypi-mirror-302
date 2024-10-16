from enum import Enum
import os
import time
from rich.console import Console
from typer import Typer, progressbar

from p12 import v12, v3120_app, v3120_app_

from .p09 import v09, v3090_app, v3090_app_


class AvailableVersions(Enum):
    Python3000 = f'{v09}.0'
    Python3120 = f'{v12}.0'

console: Console = Console(highlight=False)
app: Typer = Typer(
    name='app',
    pretty_exceptions_show_locals=False,
)
app.add_typer(v3090_app)
app.add_typer(v3090_app_)
app.add_typer(v3120_app)
app.add_typer(v3120_app_)

def show_all_versions():
    """Show all of the current versions available"""
    available_versions: list[AvailableVersions] = [
        AvailableVersions.Python3000,
        AvailableVersions.Python3120,
    ]
    for version in available_versions:
        console.print(f'[green][{version.value}][/] version = python-{version.value}')

@app.command()
def versions(
#
) -> None:
    """
    Displays a list of available versions
    """
    show_all_versions()

__all__ = [
    "app",
]

@app.command()
def use(
#
    version: AvailableVersions
) -> None:
    """
    Use the given python version or path as the base interpreter
    """
    p3k_dir = os.path.join(os.getcwd(), '.p3k')
    os.makedirs(p3k_dir, exist_ok=True)
    p3k_ver_file = os.path.join(p3k_dir, 'version')
    def update_global_version(new_version):
        for i in range(50):
            yield i
        with open(p3k_ver_file, 'w', encoding='UTF-8') as overwrite:
            overwrite.write(new_version)


    if os.path.exists(p3k_ver_file):
        with open(p3k_ver_file, 'r', encoding='UTF-8') as p3k_file:
            old_version = p3k_file.readlines()[0]

            if old_version == version.value:
                console.print(f'[red]Version {version.value} is already active[/]')
                return
            console.print(f'Old version: python-{old_version}')
    with progressbar(
        update_global_version(version.value),
        length=100,
        color=True,
        fill_char='🁢',
        label="Changing python version:",
    ) as progress:
        for _ in progress:
            time.sleep(0.015)
    console.print(f'New version: python-{version.value}')

__all__ = [
    "app",
]
