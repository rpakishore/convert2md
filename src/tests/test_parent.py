from pathlib import Path
from unittest.mock import Mock, mock_open, patch

import pytest
from rich.console import Console
from rich.panel import Panel

# Assuming the code is in a file named parent_parser.py
from convert2md.converters.parent import ParentParser


# Create a concrete class for testing since ParentParser is abstract
class ConcreteParser(ParentParser):
    def _process_file(self, filepath: Path, **kwargs) -> str:
        return "Processed content"


@pytest.fixture
def parser():
    return ConcreteParser()


@pytest.fixture
def tmp_file(tmp_path):
    file = tmp_path / "test.txt"
    file.write_text("Test content")
    return file


class TestParentParser:
    def test_initialization(self, parser):
        """Test if the parser initializes with correct attributes"""
        assert isinstance(parser._console, Console)
        assert hasattr(parser, "config")
        assert parser.VERBOSITY is False

    def test_write_method(self, tmp_path):
        """Test if _write method correctly writes content to file"""
        test_content = "Test markdown content"
        dest_path = tmp_path / "output.md"

        result = ParentParser._write(dest_path, test_content)

        assert result == dest_path
        assert dest_path.exists()
        assert dest_path.read_text(encoding="utf-8") == test_content

    @patch("rich.console.Console.status")
    @patch("rich.console.Console.print")
    def test_convert_method(self, mock_print, mock_status, parser, tmp_path):
        """Test the convert method with default destination directory"""
        # Setup
        input_file = tmp_path / "test.txt"
        input_file.write_text("Test content")

        # Create a context manager mock
        mock_status.return_value.__enter__ = Mock()
        mock_status.return_value.__exit__ = Mock()

        # Execute
        parser.convert(input_file)

        # Assert
        expected_output = tmp_path / "test.md"
        assert expected_output.exists()
        assert expected_output.read_text(encoding="utf-8") == "Processed content"

        # # Verify rich console output
        # mock_print.assert_called_once()
        # args, _ = mock_print.call_args
        # assert isinstance(args[0], Panel)
        # assert str(expected_output) in str(args[0])

    @patch("rich.console.Console.status")
    @patch("rich.console.Console.print")
    def test_convert_method_custom_dest(
        self, mock_print, mock_status, parser, tmp_path
    ):
        """Test the convert method with custom destination directory"""
        # Setup
        input_file = tmp_path / "test.txt"
        input_file.write_text("Test content")
        custom_dest = tmp_path / "custom_dir"
        custom_dest.mkdir()

        # Create a context manager mock
        mock_status.return_value.__enter__ = Mock()
        mock_status.return_value.__exit__ = Mock()

        # Execute
        parser.convert(input_file, custom_dest)

        # Assert
        expected_output = custom_dest / "test.md"
        assert expected_output.exists()
        assert expected_output.read_text(encoding="utf-8") == "Processed content"

    def test_abstract_method_enforcement(self):
        """Test that ParentParser cannot be instantiated without implementing _process_file"""
        with pytest.raises(TypeError):
            ParentParser()

    @pytest.mark.parametrize(
        "filename,expected",
        [
            ("test.txt", "test.md"),
            ("document.docx", "document.md"),
            ("report.pdf", "report.md"),
        ],
    )
    def test_output_filename_generation(self, filename, expected, parser, tmp_path):
        """Test that correct output filenames are generated for different input files"""
        input_file = tmp_path / filename
        input_file.write_text("Test content")

        with patch("rich.console.Console.status") as mock_status:
            mock_status.return_value.__enter__ = Mock()
            mock_status.return_value.__exit__ = Mock()

            parser.convert(input_file)

            expected_output = tmp_path / expected
            assert expected_output.exists()

    def test_error_handling_invalid_input(self, parser):
        """Test handling of non-existent input file"""
        with pytest.raises(AssertionError):
            parser.convert(Path("non_existent_file.txt"))
