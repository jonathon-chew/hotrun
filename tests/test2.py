import io
import pathlib
import tempfile
import unittest
from contextlib import redirect_stdout
from types import SimpleNamespace
from unittest.mock import Mock, patch

import hotrun

class PackageFunctionTests(unittest.TestCase):
    def test_get_watch_files_removes_ignored_entries(self):
        watch_files = hotrun.get_watch_files(
            ["app.py", ".git", "src", "venv", "README.md"],
            ignore=[".git", "venv"],
        )

        self.assertEqual(watch_files, ["app.py", "src", "README.md"])

    def test_check_file_updated_returns_timestamp_and_zero_for_missing(self):
        with tempfile.NamedTemporaryFile(delete=False) as handle:
            temp_path = pathlib.Path(handle.name)

        try:
            mtime = hotrun.check_file_updated(str(temp_path))
            self.assertIsInstance(mtime, float)
            self.assertGreater(mtime, 0)
            self.assertEqual(hotrun.check_file_updated(str(temp_path) + ".missing"), 0)
        finally:
            temp_path.unlink(missing_ok=True)

    def test_run_commands_appends_arguments_and_reports_stderr(self):
        fake_output = SimpleNamespace(stderr="boom\n")
        fake_runner = Mock(return_value=fake_output)
        stderr_printer = Mock()

        with redirect_stdout(io.StringIO()) as buffer:
            result = hotrun.run_commands(
                ["python", "script.py"],
                3,
                arguments=["--flag", "value"],
                debug_flags=lambda: "debug",
                stderr_printer=stderr_printer,
                runner=fake_runner,
                clock=Mock(side_effect=[10.0, 10.25]),
            )

        self.assertEqual(result, 0.25)
        fake_runner.assert_called_once_with(
            ["python", "script.py", "--flag", "value"],
            capture_output=True,
            text=True,
        )
        stderr_printer.assert_called_once_with("boom\n")
        output = buffer.getvalue().splitlines()
        self.assertEqual(output[0], "debug")
        self.assertEqual(output[-1], "✔ run #3 complete (0.25)")


if __name__ == "__main__":
    unittest.main()
