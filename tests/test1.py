import importlib.util
import pathlib
import sys
import types
import unittest
from unittest.mock import patch


ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI_PATH = ROOT / "hotrun" / "cli.py"


class FakeFlags:
    def __init__(self):
        self.add_calls = []
        self.add_file_calls = []
        self.parse_calls = []

    def add(self, *args, **kwargs):
        self.add_calls.append((args, kwargs))

    def add_file(self, *args, **kwargs):
        self.add_file_calls.append((args, kwargs))

    def parse(self, argv):
        self.parse_calls.append(list(argv))


class CliModuleTests(unittest.TestCase):
    def test_cli_registers_expected_flags_and_parses_argv(self):
        fake_flags = FakeFlags()
        fake_pyflags = types.ModuleType("pyflags")
        fake_pyflags_flag = types.ModuleType("pyflags.flag")
        fake_pyflags_flag.Flags = lambda: fake_flags
        fake_pyflags.__path__ = []
        fake_pyflags.flag = fake_pyflags_flag

        with patch.dict(
            sys.modules,
            {
                "pyflags": fake_pyflags,
                "pyflags.flag": fake_pyflags_flag,
            },
            clear=False,
        ):
            spec = importlib.util.spec_from_file_location("hotrun_cli_test", CLI_PATH)
            module = importlib.util.module_from_spec(spec)
            old_argv = sys.argv[:]
            sys.argv = ["cli.py", "--watch", "src/", "--once"]
            try:
                assert spec.loader is not None
                spec.loader.exec_module(module)
                module.cli()
            finally:
                sys.argv = old_argv

        self.assertEqual(
            [call[0][0] for call in fake_flags.add_calls],
            [
                ["--file"],
                ["--arguments"],
                ["--watch"],
                ["--ignore"],
                ["--debounce"],
                ["--clear"],
                ["--once"],
                ["--module"],
                ["--env"],
                ["--profile"],
                ["--track"],
                ["--no-diff"],
                ["--diff-mode"],
                ["--graph"],
                ["--affected"],
                ["--help"],
            ],
        )
        self.assertEqual([call[0][0] for call in fake_flags.add_file_calls], [["--python"]])
        self.assertEqual(fake_flags.parse_calls, [["--watch", "src/", "--once"]])


if __name__ == "__main__":
    unittest.main()
