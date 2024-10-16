import os
import re
from typer import Option, Typer
from rich.console import Console
from version3900 import ver

v3130_console: Console = Console(highlight=False)
v3130_app: Typer= Typer(name='p13', help='Python interpreter: 3.13.0 (alias)')
v3130_app_: Typer = Typer(name='p3130', help='Python interpreter: 3.13.0')

@v3130_app.command()
@v3130_app_.command()
def about():
    """Shows information about this app"""
    version()

@v3130_app.command()
@v3130_app_.command()
def version():
    """Shows the version of python used by this app"""
    ver('3.13.0', True, 'version = python-')

@v3130_app.command()
@v3130_app_.command()
def active(file_path: str = os.path.join('.p3k', 'version'), verbose: bool = Option(False, '--v')):
    """Displays whether this python interpreter is active for this app"""
    if '.p3k' not in file_path:
        v3130_console.print('[red]The file given was not at the correct location[/]')
        return
    if 'version' not in file_path:
        v3130_console.print('[red]The file given was not at the correct location[/]')
        return
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='UTF-8') as p3k_file:
            current_version = p3k_file.readlines()[0].strip()
            if not current_version.startswith('3'):
                v3130_console.print(
                    f'[red]Version must begin with a 3.[/]\n"{current_version}" was given.'
                    if verbose else
                    '[red]Version must begin with a 3.[/]'
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
                v3130_console.print(
                    f'[red]Version must include {{major.minor.patch}} or end in a regular flag,'
                    f'[/]\n"{current_version}" was given.'
                    if verbose else
                    '[red]Version must include {{major.minor.patch}} or end in a regular flag'
                )
                return

            if current_version == '3.13.0':
                v3130_console.print('[green]Version 3.13.0 is active.[/]')
            else:
                v3130_console.print(
                    '[red]Version 3.13.0 is inactive.[/]\n'
                    f'[green]Version {current_version} is active.[/]'
                    if verbose else
                    '[red]Version 3.13.0 is inactive.[/]'
                )
