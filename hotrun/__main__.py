import os, sys, time, subprocess

from .utils import get_watch_files, poll_changes, should_run, clear_screen
from .cli import cli as commands
from .Adonis import PrintWarning, PrintError, PrintTable

cli = commands()

if cli.help:
    cli.help_text_ordered()
    sys.exit(0)

# Quick hack for now! As the flag package isn't quite working as I would like it to 
cli.ignore.append(".git") if cli.ignore == [] else cli.ignore
    
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
            # Check both list, if anything from a is in b continue the loop
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
        self.running = False
        self.pending = False

        self._start_time = time.time()
        self._total_files_changed = 0
        self._total_execution_time = 0.0
        self._stats = {}

    def print_stats(self):
        # Print table directly - printing self._stats isn't the same...
        PrintTable({
            "Running time": round(time.time() - self._start_time, 2),
            "Total time spent executing": self._total_execution_time,
            "Total files": self._total_files_changed,
            "Arguments": cli.debug_flags()
        })
    
    def _run_commands(self):
        print(self.cli.debug_flags())
        start = time.time()

        if self.cli.module:
            commands = [sys.executable, "-m", self.cli.file]
        else:
            commands = [sys.executable, self.cli.file]

        output = subprocess.run(commands, capture_output=True, text=True)

        if output.stderr:
            PrintError(str(output.stderr))

        if output.stdout:
            print(output.stdout)
        
        self.execution_time = round(time.time() - start, 2)
        self.incriment_counters()

        # if they select profile - print the more detailed stats?!
        # Does this need to be in addition - instead of, only in the final?
        if cli.profile:
            self.print_stats() 
        print(f"✔ run #{self.counter} complete ({self.execution_time}) avg: {round(self._total_execution_time / self._total_files_changed, 5)}")
    
    def mark_change(self, count):
        self.dirty = True
        self.last_change = time.time()
        self.files_changed += count

    def reset(self):
        self.dirty = False
        self.files_changed = 0

    def incriment_counters(self):
        self.counter += 1
        self._total_execution_time += self.execution_time
        self._total_files_changed += self.files_changed

    def run(self):
        self.running = True
        try:
            if self.cli.clear:
                clear_screen()
        
            print(f"files changed: {self.files_changed}")
            print("────────────────────────────")
            try:
                self._run_commands()
            except Exception as e:
                PrintError(str(e))
            print("────────────────────────────")

            # time.sleep(10.0)
            print("watching for changes...")
        finally:
            self.running = False


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
        if state.running:
            state.pending = True
        else:
            state.mark_change(len(set(changed)))

    if state.dirty and not state.running and (now - state.last_change > cli.debounce):
        state.run()

        if state.pending:
            state.last_change = time.time()
            state.dirty = True
            state.pending = False
        else:
            state.reset()

        if cli.once:
            print(f"✔ complete ({state.execution_time})") # type: ignore
            sys.exit(0)

    time.sleep(0.1)