from pathlib import Path
import re
from typing import Literal
import shutil

root_dir = Path(__file__).parent.parent
read_me: Path = root_dir / 'README.md'
project_path: Path = root_dir / 'src' / 'convert2md'
tests_path: Path = root_dir / 'src' / 'tests'
pyproject: Path = root_dir / 'pyproject.toml'
config:Path = root_dir / 'config.example.toml'

#Get acceptable package name for future use
def acceptable_pkg_name(name:str) -> str:
    accepted: bool = False
    while not accepted:
        blacklist: list[str] = [" ", "-", '"', "'"]
        accepted = True
        for char in blacklist:
            if char in name:
                print(f"{name} is not an acceptable package name. Found char \"{char}\".")
                name = input("Try again: ").strip()
                accepted = False
                break
    return name

urlname: str = input("Enter the \"Package\" name").strip()
package = acceptable_pkg_name(name=urlname)

# Ask if specific functionality is needed and trim accordingly
def ask_yes_no(q: str) -> bool:
    """Asks the questions and collects y/n response"""
    accepted: bool = False
    while not accepted:
        response = input(f"{q} [Y/n]").strip().lower()
        if response in ["y", "n", ""]:
            accepted = True
        else:
            print(f"Invalid response: {response}")
    return response == "y" or response == ""

def replace_txt_in_file(filepath: Path, match: str, replacement: str, match_type: Literal['txt', 're']= 'txt') -> bool:
    """Replace a text in file if it exists"""
    with open(filepath, 'r', encoding="utf-8") as f:
        contents = f.read()
    
    if match_type == 're':
        matches = re.match(pattern=match, string=contents)
    elif match_type == 'txt':
        matches = match in contents
    
    if matches:
        if match_type == 're':
            new_content = re.sub(match, replacement, contents)
        elif match_type == 'txt':
            new_content = contents.replace(match, replacement)
        with open(filepath, 'w', encoding="utf-8") as f:
            f.write(new_content)
        return True
    else:
        return False
    
if not ask_yes_no("Public Repo?"):
    replace_txt_in_file(file=read_me, match=r"^!\[[\w\s]*\]\(.*\)$", replacement="", match_type="re")

if not ask_yes_no("Need Cryptography?"):
    shutil.rmtree(path=(project_path  / 'cryptography'))
    (tests_path / 'test_cryptography.py').unlink()
    replace_txt_in_file(filepath=pyproject, match='"cryptography",', replacement="")

if not ask_yes_no("Need Slack?"):
    (project_path / 'notify' / 'Slack.py').unlink()
    replace_txt_in_file(filepath=pyproject, match='"slack_sdk",', replacement="")

if not ask_yes_no("Need Gotify?"):
    (project_path / 'notify' / 'Gotify.py').unlink()
    replace_txt_in_file(filepath=pyproject, match='"ak_requests",', replacement="")

    _replace = """    # Gotify
    check_configs("Gotify", [("gotify", "app")])
"""
    replace_txt_in_file(filepath=(project_path / '__init__.py'), match=_replace, replacement="")
    

if not ask_yes_no("Need CLI?"):
    (project_path / 'cli_app.py').unlink()
    replace_txt_in_file(filepath=pyproject, match='app="convert2md.cli_app:app"', replacement="")
    
if not ask_yes_no("Need LLM?"):
    (project_path / 'llm.py').unlink()
    replace_txt_in_file(filepath=pyproject, match='"ollama",', replacement="")
    replace_txt_in_file(filepath=pyproject, match='"tiktoken",', replacement="")
    replace_txt_in_file(filepath=pyproject, match='"openai",', replacement="")
    replace_txt_in_file(filepath=pyproject, match='"instructor",', replacement="")
    replace_txt_in_file(filepath=pyproject, match='"pydantic",', replacement="")
    
    _replace="""[openai]
api_base='http://localhost:11434/v1'
key='ollama' #base64 encoded key
model='llama3'
"""
    replace_txt_in_file(filepath=config, match=_replace, replacement="")
    
    _replace = """    # OpenAI
    check_configs(
        "OpenAI", [("openai", "api_base"), ("openai", "key"), ("openai", "model")]
    )
"""
    replace_txt_in_file(filepath=(project_path / '__init__.py'), match=_replace, replacement="")
    
    if not ask_yes_no("Need Credentials?"):
        (project_path / 'utils' /'credentials.py').unlink()
        (tests_path /'test_credentials.py').unlink()
        replace_txt_in_file(filepath=pyproject, match='"keyring",', replacement="")
    
project_path.rename(project_path.with_name(package))

#replace all convert2md reference with package_name
exts = [".toml", ".json", ".txt", ".py", ".md"]
for ext in exts:
    for file in root_dir.glob(f"**/*{ext}"):
        replace_txt_in_file(filepath=file, match="rpakishore/convert2md", replacement=f"rpakishore/{urlname}")
        replace_txt_in_file(filepath=file, match="convert2md", replacement=package)

# delete current file
Path(__file__).unlink()