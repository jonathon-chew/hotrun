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

def run_commands(state) -> float:
    print(state.cli.debug_flags())
    start = time.time()

    if state.cli.module:
        commands = [sys.executable, "-m", state.cli.file]
    else:
        commands = [sys.executable, state.cli.file]

    output = subprocess.run(commands, capture_output=True, text=True)

    if output.stderr:
        PrintError(str(output.stderr))

    if output.stdout:
        print(output.stdout)
    
    state.execution_time = round(time.time() - start, 2)

    print(f"✔ run #{state.counter} complete ({state.execution_time})")
    
    return round(time.time() - start, 2)

def poll_changes(watch_files: list[str], last_updated: dict[str, float]) -> list[str]:
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

def orchestrate(state):
    if state.cli.clear:
        clear_screen()
    
    print(f"files changed: {state.files_changed}")
    print("────────────────────────────")
    state.execution_time = run_commands(state)
    state.incriment_counter()
    print("────────────────────────────")

    # time.sleep(10.0)
    print("watching for changes...")

    return