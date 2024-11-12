import getpass
import sys
from base64 import b64decode, b64encode

from convert2md import _config


def get_password(item: str, username: str):
    """Retrieve password from Keyring(if exist, else prompt for password)"""

    # Check the `config.toml` file
    pwd = _config.get(keys=(item, username), default="")
    if pwd != "":
        return pwd

    if sys.platform == "win32":
        import keyring

        log.debug(f"getting pwd for `{username}` in `{item}`")
        pwd = keyring.get_password(item, username)
        if not pwd:
            log.warning("Password is not saved in keyring.")
            pwd = getpass.getpass(
                f"Enter the password for {item} corresponding to Username:{username}: "
            )

            choice: str = input("Save to keyring? (y/N): ")
            if choice.strip().casefold() == "y":
                save_password(item=item, username=username, pwd=pwd)
    else:
        pwd = getpass.getpass(
            f"Enter the password for `{item}` corresponding to Username:`{username}`  : "
        )

    return pwd


def save_password(item: str, username: str, pwd: str):
    """Saves the password to keyring"""
    assert sys.platform == "win32"
    import keyring

    keyring.set_password(item, username, pwd)
    log.info(f"Password for {item}/{username} saved to keyring")


def encode(text: str) -> str:
    return b64encode(text.encode()).decode()


def decode(text: str) -> str:
    return b64decode(text.encode()).decode()
