from pathlib import Path
from abc import ABC, abstractmethod
from rich.console import Console
from rich.panel import Panel
from rich import print
from typing import Literal

from convert2md import _config
from .doclingparser import DoclingParser
from .llamaparse import LlamaParser

Parser = LlamaParser | DoclingParser


def Convert(filepath: str | Path, **kwargs):
    if isinstance(filepath, str):
        filepath = Path(filepath.replace('"', "").strip())

    parser = _select_parser(filepath=filepath, **kwargs)
    parser.convert(filepath=filepath, **kwargs)


def _select_parser(filepath: Path, **kwargs) -> Parser:
    if "parser" in kwargs.keys():
        match kwargs["parser"].casefold():
            case "llamaparser":
                return LlamaParser()

            case "doclingparser":
                return DoclingParser()

            case _:
                raise Exception(f"{kwargs['parser']} is not a valid input for `parser`")
    else:
        if (
            filepath.suffix.casefold() == ".pdf"
            and _config.get(keys=("llamaparser", "apiKey"), default="") != ""
        ):
            return LlamaParser()
        else:
            return DoclingParser()
