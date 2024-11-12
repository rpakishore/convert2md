from pathlib import Path
from typing import Literal

import nest_asyncio
import requests
from llama_parse import LlamaParse, ResultType
from rich.progress import BarColumn, Progress


from .parent import ParentParser


nest_asyncio.apply()


class LlamaParser(ParentParser):
    def __init__(self) -> None:
        super().__init__()

    def __parser(self, result_type: Literal[".md", ".txt"], **kwargs):
        verbose = self.VERBOSITY
        match result_type.casefold():
            case ".md":
                _result_type = ResultType.MD
            case ".txt":
                _result_type = ResultType.TXT
            case _:
                raise Exception(f"{result_type=} not in `Literal['.md', '.txt']`")

        _default_args = {
            "api_key": self.config.get(keys=("llamaparse", "apiKey")),
            "result_type": _result_type,
            "verbose": verbose,
            "parsing_instruction": "",
            "skip_diagonal_text": False,
            "do_not_unroll_columns": False,
        }

        for k, v in kwargs:
            _default_args[k] = v

        return LlamaParse(**_default_args)

    def _process_file(
        self, filepath: Path, result_type: Literal[".md", ".txt"], **kwargs
    ) -> str:
        docs = self.__parser(result_type=result_type, **kwargs).load_data(str(filepath))
        response: str = "\n".join([doc.text for doc in docs])
        self.__check_usage(self)
        return response

    def __check_usage(self):

        url = "https://api.cloud.llamaindex.ai/api/v1/parsing/usage"

        payload = {}
        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {self.config.get(keys=('llamaparse', 'apiKey'))}",
        }
        response = requests.request("GET", url, headers=headers, data=payload).json()

        # Example values for pages used and remaining
        pages_used = response.get("usage_pdf_pages")
        total_pages = response.get("max_pdf_pages")

        # Display a static bar with no live update
        progress = Progress(
            "[bold cyan]Pages Used:[/bold cyan] {task.completed} / {task.total}",
            BarColumn(bar_width=40),
            "[progress.percentage]{task.percentage:>3.0f}%",
        )

        # Add the static task for the progress bar
        progress.add_task("Used", total=total_pages, completed=pages_used)

        # Render the progress bar to the console
        self._console.print(progress)
