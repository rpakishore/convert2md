import typer
from rich.console import Console

from .utils.credentials import save_password as save_pwd
from .utils.logger import log

from template_python import test_configs

app = typer.Typer()
console = Console()


@app.command()
def template_fn(template_str: str, template_bool: bool = False):
    """This is a sample function to be executed through the cli app"""
    log.info("Called the `template_fn` function")


@app.command()
def save_password(item: str, username: str, pwd: str):
    """Saves password to keyring"""
    try:
        save_pwd(item, username, pwd)
        console.print("Password saved to keyring", style="rgb(73,175,65)")
    except Exception as e:
        console.print("Error occured when saving to keyring", style="rgb(242,16,59)")
        console.print(str(e))


@app.command()
def encode_base64(text: str) -> str:
    """converts base string to base64 string. Useful for filling out `config.toml`"""
    import base64

    return base64.b64encode(text.encode()).decode()

test = typer.Typer()

@test.command()
def test():
    test_configs()