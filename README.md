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

### Install from GitHub

You can install `hotrun` straight from the GitHub repository with pip:

```bash
pip install git+https://github.com/jonathon-chew/hotrun.git
```

If you want to pin a specific version, replace `main` with a tag or commit hash:

```bash
pip install git+https://github.com/jonathon-chew/hotrun.git@main
```

The project currently exposes its entrypoint through the package module:

```bash
python3 -m hotrun script.py
```

With arguments:

```bash
python3 -m hotrun script.py --arguments arg1 arg2
```

## Example Workflow

`hotrun` shines when you are making repeated edits and want the next run to happen automatically. It is especially useful when the thing you are changing is small enough that restarting it by hand would slow you down more than the code itself.

### Fast API or web app iteration

```bash
python3 -m hotrun app.py --watch app.py src/ tests/ --ignore .git venv __pycache__ --debounce 0.5
```

Use this when you are tweaking request handlers, service code, templates, or test helpers and want a quick rerun after every save.

Good fit for:
- Flask or FastAPI prototypes
- small internal tools
- backend endpoints with a few support modules

### Data scripts and automation jobs

```bash
python3 -m hotrun scripts/rebuild_report.py --watch scripts/ data/ configs/ --ignore .git venv --once
```

This works well for report builders, file transforms, import jobs, and any repeatable command that depends on local inputs or config files.

Good fit for:
- CSV or JSON transformations
- scheduled job prototypes
- one-off maintenance scripts you keep refining

### Package modules and library entrypoints

```bash
python3 -m hotrun hotrun.worker --module --watch hotrun/ --ignore .git venv --profile
```

Use module mode when the code you are changing lives inside a package and you want to exercise the package the same way your users or tests will.

Where `hotrun` tends to shine most:
- frequent save-and-check loops
- scripts that are annoying to relaunch manually
- local tooling and automation
- workflows where you care about output and iteration speed more than stepping through a debugger

## CLI Surface

The current CLI definitions include:
- `--arguments`
- `--watch`
- `--ignore`
- `--debounce`
- `--clear`
- `--once`
- `--module`
- `--env`
- `--python`
- `--profile`

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
