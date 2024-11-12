from pathlib import Path
from abc import ABC, abstractmethod
from rich.console import Console
from rich.panel import Panel
from rich import print

from convert2md import Config


class ParentParser(ABC):
    VERBOSITY: bool = False

    def __init__(self) -> None:
        self._console = Console()
        self.config = Config()

    @staticmethod
    def _write(dest_path: Path, contents: str) -> Path:
        """Write the contents of markdown document to file"""

        with open(dest_path, "w", encoding="utf-8") as f:
            f.write(contents)
        return dest_path

    @abstractmethod
    def _process_file(self, filepath: Path) -> str:
        print("Not Implemented. Converts file to `md` string")

    def convert(
        self,
        filepath: Path,
        dest_dir: Path | None = None,
        **kwargs,
    ):
        dest_dir = dest_dir or filepath.parent
        destpath: Path = dest_dir / f"{filepath.stem}.md"
        with self._console.status(
            f"Converting {filepath.name} to {destpath.name}...", spinner="dots"
        ):
            _data = self._process_file(filepath=filepath, **kwargs)

        self._write(dest_path=destpath, contents=_data)
        self._console.print(
            Panel(
                f'[green bold]Contents written to "{str(destpath)}"',
                title="Success",
                border_style="green",
            )
        )
