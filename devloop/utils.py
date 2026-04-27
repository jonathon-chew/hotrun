import os
import subprocess
import time
import sys

from typing import Any
from .Adonis import PrintError

def clear_screen():
    if os.name == "nt":
        subprocess.run("cls", shell=True)
    else:
        subprocess.run("clear")

def get_watch_files(files_to_watch: list[str], cli: Any) -> list[str]:
    returned_files = files_to_watch.copy()
    if cli.ignore:
        for eachFile in cli.ignore:
            if eachFile in returned_files:
                returned_files.remove(eachFile)
    return returned_files

def check_file_updated(file_path: str) -> float:
    try:
        return os.path.getmtime(filename=file_path)
    except FileNotFoundError:
        raise FileNotFoundError
    except Exception as e:
        raise ValueError(e)

def run_commands(counter: int, cli: Any) -> float:
    print(cli.debug_flags())
    start = time.time()

    if cli.module:
        commands = [sys.executable, "-m", cli.file]
    else:
        commands = [sys.executable, cli.file]

    output = subprocess.run(commands, capture_output=True, text=True)

    if output.stderr:
        PrintError(str(output.stderr))

    if output.stdout:
        print(output.stdout)

    print(f"✔ run #{counter} complete ({round(time.time() - start, 2)})")
    
    return round(time.time() - start, 2)

def poll_changes(watch_files: list[str], last_updated: dict[str, float]):
    changed = []
    for i in watch_files:
        try:
            file_update_time = check_file_updated(i)
        except FileNotFoundError:
            continue
        if file_update_time > last_updated[i]:
            changed.append(i)
            last_updated[i] = file_update_time
    
    return changed

def should_run(changed_files):
    return len(changed_files) > 0