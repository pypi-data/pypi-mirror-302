import os
import re
from typer import Option, Typer
from rich.console import Console
from version3900 import build_name, ver

from .twelve import v12


v3120_console: Console = Console(highlight=False)
v3120_app: Typer= Typer(name='p12', help='Python interpreter: 3.12.0 (alias)')
v3120_app_: Typer = Typer(name='p3120', help='Python interpreter: 3.12.0')

@v3120_app.command()
@v3120_app_.command()
def about():
    """Shows information about this app"""
    version()

@v3120_app.command()
@v3120_app_.command()
def version(show_name: bool = False):
    """Shows the version of python used by this app"""
    if show_name:
        v3120_console.print(f'[blue1]version_name = [italic]python-{build_name(v12)}[/][/]')
    ver(v12, True, 'version = python-')

@v3120_app.command()
@v3120_app_.command()
def active(
    file_path: str = os.path.join('.p3k', 'version'),
    verbose: bool = Option(False, '--verbose', '-v')
):
    """Displays whether this python interpreter is active for this app"""
    if '.p3k' not in file_path:
        v3120_console.print('[red]The file given was not at the correct location[/]')
        return
    if 'version' not in file_path:
        v3120_console.print('[red]The file given was not at the correct location[/]')
        return
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='UTF-8') as p3k_file:
            current_version = p3k_file.readlines()[0].strip()
            if not current_version.startswith('3'):
                v3120_console.print(
                    f'[red]Version must begin with a 3,[/]\n"{current_version}" was given'
                    if verbose else
                    '[red]Version must begin with a 3[/]'
                )
                return

            semver_pattern = re.compile(
                r"^(?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)"
                r"(?:-(?P<label>(alpha|beta|dev|rc)(?:\d+(\.\d+)?[a-z]?)?))?$"
            )
            pattern_match = semver_pattern.match(current_version)
            if not (
                current_version.endswith('-alpha') or
                current_version.endswith('-beta') or
                current_version.endswith('-dev') or
                pattern_match
            ):
                v3120_console.print(
                    f'[red]Version must include {{major.minor.patch}} or end in a regular flag,'
                    f'[/]\n"{current_version}" was given'
                    if verbose else
                    '[red]Version must include {{major.minor.patch}} or end in a regular flag'
                )
                return

            if current_version == '3.12.0':
                v3120_console.print('[green]Version 3.12.0 is active[/]')
            else:
                v3120_console.print(
                    '[red]Version 3.12.0 is inactive[/]\n'
                    f'[green]Version {current_version} is active[/]'
                    if verbose else
                    '[red]Version 3.12.0 is inactive[/]'
                )
    else:
        v3120_console.print(
            '[red dim]Warning! No version is specified in this directory[/]\n'
            '[red]Version 3.12.0 is inactive[/]'
            if verbose else
            '[red]Version 3.12.0 is inactive[/]'
        )
