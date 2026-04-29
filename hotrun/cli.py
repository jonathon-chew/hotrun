import sys
from .pyflags.flag import Flags

def cli() -> Flags:
    flag = Flags()

    flag.add(["--file"], "File you want to run if one of the watch file changes", str, default=sys.argv[1])
    flag.add(["--arguments"], "List of arguments that need to be passed in to modify the script's behaviour", list[str])
    flag.add(["--watch"], "Which files to watch", list[str])
    flag.add(["--ignore"], "List of files to ignore", list[str], default=[".git", "venv"])
    flag.add(["--debounce"], "The amount of time to check if the file has changed", float, default=2, validator=lambda x: x > 0.0)
    flag.add(["--no-diff"], "", bool)
    flag.add(["--clear"], "Clear the screen between printing so only the last test is visible", bool, default=True)
    flag.add(["--once"], "Only run this once, dry run / testing the set up", bool)
    flag.add(["--module"], "Run the said file as a python module instead of as a script", bool)
    flag.add(["--env"], "The list of environment variables to set API_KEY=X", list[str], validator=lambda x: "=" in x)
    flag.add_file(["--python"], "which python to use - defaults to the current one in the shell, inc. if a venv is active or not", validator=lambda x: "python" in x)
    flag.add(["--profile"], "Print out some more detailed stats", bool)

    # To be implimented
    flag.add(["--track"], "", bool)
    flag.add(["--diff-mode"], "", bool, choices=["full", "simple", "none"])
    flag.add(["--graph"], "", str)
    flag.add(["--affected"], "", bool)

    flag.add(["--help"], "See the possible flags", bool)

    flag.parse(sys.argv[1:])

    return flag

cli()

"""
1. Script + args
devloop script.py -- arg1 arg2
2. --watch (optional override)
devloop script.py --watch src/ tests/

Default:

auto-detect project root
ignore .git, venv, etc.
3. --ignore
devloop script.py --ignore data/ logs/
4. --debounce
devloop script.py --debounce 200

(milliseconds)

5. --no-diff

Turn off your key feature if needed:

devloop script.py --no-diff
6. --clear

Clear terminal between runs:

devloop script.py --clear
7. --once

Run once, no watching (useful for consistency):

devloop script.py --once
🧠 Slightly more advanced (still reasonable)
8. --module

Run as module:

devloop -m mypackage.script -- arg1

Equivalent to:

python -m mypackage.script
9. --env

Inject env vars:

devloop script.py --env DEBUG=1 --env API_URL=...
10. --python

Custom interpreter:

devloop script.py --python .venv/bin/python
🔥 Your differentiator flags

These support your unique ideas:

11. --track

Explicitly track variables (if you support patterns later):

devloop script.py --track x,y,result

(works alongside a track() API)

12. --diff-mode

Control how diffs are shown:

devloop script.py --diff-mode simple
devloop script.py --diff-mode full
devloop script.py --diff-mode none
13. --profile

Basic timing info:

devloop script.py --profile

Output:

Run #5 | 0.42s (avg: 0.38s)
🧪 Optional (future, don’t build yet)
14. --graph

Debug dependency graph:

devloop script.py --graph
15. --affected

Only rerun if relevant files changed:

devloop script.py --affected

(This becomes meaningful once your dependency graph exists)
"""