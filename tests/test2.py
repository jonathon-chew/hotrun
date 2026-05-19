import io
import os
import pathlib
import tempfile
import unittest
from types import SimpleNamespace

import hotrun

class PackageFunctionTests(unittest.TestCase):
    def test_get_watch_files_removes_ignored_entries(self):
        watch_files = hotrun.get_watch_files(
            ["app.py", ".git", "src", "venv", "README.md"],
            SimpleNamespace(ignore=[".git", "venv"]),
        )

        self.assertEqual(watch_files, ["app.py", "src", "README.md"])

    def test_check_file_updated_returns_timestamp_and_raises_for_missing(self):
        with tempfile.NamedTemporaryFile(delete=False) as handle:
            temp_path = pathlib.Path(handle.name)

        try:
            mtime = hotrun.check_file_updated(str(temp_path))
            self.assertIsInstance(mtime, float)
            self.assertGreater(mtime, 0)
            with self.assertRaises(FileNotFoundError):
                hotrun.check_file_updated(str(temp_path) + ".missing")
        finally:
            temp_path.unlink(missing_ok=True)

    def test_poll_changes_detects_updates_and_should_run_flags_them(self):
        with tempfile.NamedTemporaryFile(delete=False) as handle:
            temp_path = pathlib.Path(handle.name)

        try:
            last_updated = {str(temp_path): hotrun.check_file_updated(str(temp_path))}
            changed = hotrun.poll_changes([str(temp_path)], last_updated)
            self.assertEqual(changed, [])

            os.utime(temp_path, (last_updated[str(temp_path)] + 10, last_updated[str(temp_path)] + 10))
            changed = hotrun.poll_changes([str(temp_path)], last_updated)
            self.assertEqual(changed, [str(temp_path)])
            self.assertTrue(hotrun.should_run(changed))
        finally:
            temp_path.unlink(missing_ok=True)


if __name__ == "__main__":
    unittest.main()
