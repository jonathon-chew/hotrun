# Hotrun

## Summary
`hotrun` is a small Python watcher that reruns a script when files change. The project is aiming for a developer-friendly loop for local iteration: run a script, watch relevant files, and surface useful feedback without making the terminal feel noisy.

## What This Project Demonstrates
- Python command-line parsing and script entrypoints
- file watching based on modification times
- process execution and restart loops
- simple terminal UX for rerunning a script
- space for richer output handling such as diffs, profiles, and tracked state

## Current Features
- run a target Python script repeatedly while watching files
- support an explicit watch list
- support ignored paths
- support a configurable debounce delay
- support a one-shot mode
- support running a module with `-m`
- support clearing the screen between runs
- support an interpreter override
- support optional environment and advanced workflow flags in the CLI surface

## Behavior Notes
- When no watch list is provided, the tool falls back to the current directory.
- Ignored entries are removed from the watch list before file filtering happens.
- The current loop checks file modification times and reruns the target when a change is detected.
- The current code prints stderr from the child process if the script writes any.
- `--once` is intended to run a single change cycle and then exit.

## How To Run

The project currently exposes its entrypoint through the package module:

```bash
python3 -m hotrun script.py
```

With arguments:

```bash
python3 -m hotrun script.py -- arg1 arg2
```

Example watch mode:

```bash
python3 -m hotrun script.py --watch src/ tests/
```

Example one-shot mode:

```bash
python3 -m hotrun script.py --once
```

## Example Workflow

```bash
python3 -m hotrun app.py --watch app.py src/ --ignore .git venv --debounce 0.5
```

Typical intent:
- start the watcher
- run `app.py`
- restart when a watched file changes
- keep the terminal readable between runs

## CLI Surface

The current CLI definitions include:
- `--arguments`
- `--watch`
- `--ignore`
- `--debounce`
- `--no-diff`
- `--clear`
- `--once`
- `--module`
- `--env`
- `--python`
- `--track`
- `--diff-mode`
- `--profile`
- `--graph`
- `--affected`

Some of these are part of the intended product direction rather than a fully finished user experience yet.

## Why This Is Different

Most simple file watchers stop at "rerun on save." `hotrun` is trying to become more opinionated than that:
- show the command that ran
- keep restart behavior understandable
- preserve a clean loop for repeated local edits
- make room for meaningful diff and profiling output
- support future stateful workflows like argument reuse and dependency-aware reruns

## Testing

The project has tests under `tests/`.

Run them with:

```bash
python3 -m unittest discover -s tests
```