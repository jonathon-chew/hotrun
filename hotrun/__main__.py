import os, sys, time

from .utils import get_watch_files, poll_changes, should_run, orchestrate
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
            full_path = os.path.join(root, name)
            split_file_path = full_path.split(os.sep)
            if any(i in cli.ignore for i in split_file_path):
                continue
            file_dir.append(full_path)

    watch_files = get_watch_files(file_dir, cli)

watch_files = [ f for f in watch_files if os.path.isfile(f) ]

if len(watch_files) < 1:
    PrintError("[Error]: No files found to watch")
    sys.exit(1)

## Finished basic set up - let's start setting the state of the programme!
print("[hotrun] starting...")

class State:
    def __init__(self):
        self.counter = 1
        self.last_updated = {}
        self.last_change = time.time()
        self.dirty = False # key flag for tracking state
        self.files_changed = 0 # debounce means I need to track this
        self.cli = cli
        self.execution_time = 0.0

        self._start_time = time.time()
        self._total_files_changed = 0
    
    def mark_change(self, count):
        self.dirty = True
        self.last_change = time.time()
        self.files_changed += count
        self._total_files_changed += count

    def reset(self):
        self.dirty = False
        self.files_changed = 0

    def incriment_counter(self):
        self.counter += 1

state = State()

for f in watch_files:
    try:
        state.last_updated[f] = os.path.getmtime(f)
    except:
        state.last_updated[f] = 0

while True:
    
    # returns an array - so number of files changed can be used as a metric and presented to the user, also could be used for tracking / logging later on
    changed = poll_changes(watch_files, state.last_updated) 
    now = time.time() # set every time as needs to be tracked

    if should_run(changed):
        state.mark_change(len(set(changed)))

    if state.dirty and (now - state.last_change > cli.debounce):
        orchestrate(state)
        state.reset()

    if cli.once and should_run(changed):
        print(f"✔ complete complete ({state.execution_time})") # type: ignore
        sys.exit(0)

    time.sleep(0.1)