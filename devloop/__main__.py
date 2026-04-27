import os, sys, subprocess, time

import cli, Adonis

def clear_screen():
    if os.name == "nt":
        subprocess.run("cls", shell=True)
    else:
        subprocess.run("clear")

def get_watch_files(files_to_watch: list[str]) -> list[str]:
    returned_files = files_to_watch.copy()
    if cli.flag.ignore:
        for eachFile in cli.flag.ignore:
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

def run_commands(commands: list[str], counter: int) -> float:
    print(cli.flag.debug_flags())
    start = time.time()
    output = subprocess.run(commands, text=True)

    if output.stderr is not None:
        Adonis.PrintError(str(output.stderr))

    print(f"✔ run #{counter} complete ({time.time() - start})")
    
    return time.time() - start

if not cli.flag.watch:
    Adonis.PrintWarning("⚠ no project root detected")
    print(f"using current directory:{os.path.dirname(os.path.realpath(__file__))}")
    watch_files = get_watch_files(os.listdir("."))
else:
    watch_files = get_watch_files(cli.flag.watch)

watch_files = [ f for f in watch_files if os.path.isfile(f) ]

if len(watch_files) < 1:
    Adonis.PrintError("[Error]: No files found to watch")
    sys.exit(1)

print("[devloop] starting...")
counter = 1
last_updated = {}
for f in watch_files:
    try:
        last_updated[f] = os.path.getmtime(f)
    except:
        last_updated[f] = 0

while True:

    file_updated = False
    for i in watch_files:
        try:
            file_update_time = check_file_updated(i)
        except FileNotFoundError:
            continue
        if file_update_time > last_updated[i]:
            file_updated = True
            last_updated[i] = file_update_time

    if file_updated:
        print("────────────────────────────")
        if cli.flag.clear:
                clear_screen()

        if cli.flag.module:
            run_time = run_commands([sys.executable, "-m", cli.flag.file], counter)
            counter += 1
        else:
            run_time = run_commands([sys.executable, cli.flag.file], counter)
            counter += 1
        print("────────────────────────────")

        time.sleep(10.0)
        print("watching for changes...")

    if cli.flag.once and file_updated == True:
        assert isinstance(run_time, float) #type: ignore
        print(f"✔ complete complete ({run_time})")
        sys.exit(0)

    time.sleep(cli.flag.debounce)