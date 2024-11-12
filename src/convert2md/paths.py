from pathlib import Path

_this = Path(__file__)
pkg_dir = _this.parent
src_dir = pkg_dir.parent
tests_dir = src_dir / "tests"
