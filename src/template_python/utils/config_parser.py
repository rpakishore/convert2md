import tomllib
from functools import cached_property
from pathlib import Path

from .logger import log


class Config:
    def __init__(
        self, filename: str = "config.toml", filepath: Path | None = None
    ) -> None:
        self.__filename = filename
        self.__filepath: Path | None = None
        if filepath is not None:
            if filepath.is_dir():
                self.__filepath = filepath / filename
            else:
                self.__filename = filepath.name
        log.info(f"Initialized {self.__str__()}. Config Exists: {self.exists()}.")

    def __str__(self) -> str:
        return f"Config(filename={self.__filename}, filepath={self.__filepath})"

    @cached_property
    def filepath(self) -> Path | None:
        if self.__filepath is not None and self.filepath.exists():
            return self.__filepath
        if Path(self.__filename).exists():
            return Path(self.__filename)

        src_path = self.__find_src_folder()
        if src_path is not None:
            return src_path / self.__filename

        return None

    def __find_src_folder(self) -> Path | None:
        filepath = Path(__file__).resolve()
        fileparts = filepath.parts
        if "src" in fileparts:
            src_index = fileparts.index("src")
            return Path(*filepath.parts[:src_index])
        else:
            return None

    @property
    def value(self) -> dict:
        """Get config value"""
        if self.filepath is not None and self.filepath.exists():
            with open(self.filepath, "r") as f:
                return tomllib.loads(f.read())
        return {}

    def get(self, keys: tuple[str, ...], default=None):
        """Get the value from config"""
        data = self.value
        for key in keys[:-1]:
            data = data.get(key, {})
        return data.get(keys[-1], default)

    def exists(self) -> bool:
        if self.filepath is None:
            return False
        if not self.filepath.exists():
            return False
        return True
