import typer
from rich import print

from convert2md import test_configs

from .utils.credentials import save_password as save_pwd
from convert2md.converters.main import Convert

app = typer.Typer()


@app.command()
def convert(filepath: str):
    Convert(filepath=filepath)


test = typer.Typer()


@test.command()
def test():
    test_configs()
