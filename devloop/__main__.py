import os, sys, subprocess, time

from .utils import get_watch_files, clear_screen, check_file_updated, run_commands, poll_changes, should_run
from .cli import cli as commands
from .Adonis import PrintWarning, PrintError

cli = commands()

if cli.help:
    cli.help_text_ordered()
    sys.exit(0)

if cli.watch:
    watch_files = get_watch_files(cli.watch, cli)
else:
    PrintWarning("⚠ no project root detected")
    print(f"using current directory:{os.path.dirname(os.path.realpath(__file__))}")
    file_dir = []
    for root, dirs, files in os.walk("."):
        for name in files:
            if dirs not in cli.ignore or files not in cli.ignore or root not in cli.ignore: # ignore files/folders that should be!
                file_dir.append(os.path.join(root, name))
    watch_files = get_watch_files(file_dir, cli)

watch_files = [ f for f in watch_files if os.path.isfile(f) ]

if len(watch_files) < 1:
    PrintError("[Error]: No files found to watch")
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

    changed = poll_changes(watch_files, last_updated)

    if should_run(changed):
        print("────────────────────────────")
        if cli.clear:
            clear_screen()

        run_time = run_commands(counter, cli)
        counter += 1
        print("────────────────────────────")

        # time.sleep(10.0)
        print("watching for changes...")

    if cli.once and should_run(changed):
        assert isinstance(run_time, float) #type: ignore
        print(f"✔ complete complete ({run_time})")
        sys.exit(0)

    time.sleep(cli.debounce)