import sys
from pyflags.flag import Flags

flag = Flags()

flag.add([" --watch"], "", list[str])
flag.add([" --ignore"], "", list[str], default=[".git", "venv"])
flag.add([" --debounce"], "", float, default=2, validator=lambda x: x > 0.0)
flag.add([" --no-diff"], "", bool)
flag.add([" --clear"], "", bool, default=True)
flag.add([" --once"], "", bool)
flag.add([" --module"], "", bool)
flag.add([" --env"], "", list[str])
flag.add_file([" --python"], "")
flag.add([" --track"], "", bool)
flag.add([" --diff-mode"], "", bool, choices=["full", "simple", "none"])
flag.add([" --profile"], "", str)
flag.add([" --graph"], "", str)
flag.add([" --affected"], "", bool)

flag.parse(sys.argv[1:])

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