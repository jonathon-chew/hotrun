from __future__ import annotations

import base64
import csv
import hashlib
import os
from pathlib import Path
import tempfile
import zipfile

NAME = "hotrun"
VERSION = "0.3.4"
TAG = "py3-none-any"
DIST_INFO = f"{NAME}-{VERSION}.dist-info"
WHEEL_NAME = f"{NAME}-{VERSION}-{TAG}.whl"


def _project_root() -> Path:
    return Path(__file__).resolve().parent


def _package_files() -> list[Path]:
    root = _project_root() / "hotrun"
    files: list[Path] = []
    for path in root.rglob("*.py"):
        if "__pycache__" in path.parts:
            continue
        files.append(path)
    return files


def _metadata_text() -> str:
    return "\n".join(
        [
            "Metadata-Version: 2.1",
            f"Name: {NAME}",
            f"Version: {VERSION}",
            "Summary: A Python watcher that reruns scripts when files change",
            "",
        ]
    )


def _wheel_text() -> str:
    return "\n".join(
        [
            "Wheel-Version: 1.0",
            "Generator: hotrun.build_backend",
            "Root-Is-Purelib: true",
            f"Tag: {TAG}",
            "",
        ]
    )


def _entry_points_text() -> str:
    return "\n".join(
        [
            "[console_scripts]",
            "hotrun = hotrun.__main__:main",
            "",
        ]
    )


def _top_level_text() -> str:
    return "hotrun\n"


def _hash_bytes(data: bytes) -> str:
    digest = hashlib.sha256(data).digest()
    encoded = base64.urlsafe_b64encode(digest).rstrip(b"=").decode("ascii")
    return f"sha256={encoded}"


def _write_metadata_dir(metadata_directory: str) -> Path:
    dist_info = Path(metadata_directory) / DIST_INFO
    dist_info.mkdir(parents=True, exist_ok=True)
    (dist_info / "METADATA").write_text(_metadata_text(), encoding="utf-8")
    (dist_info / "WHEEL").write_text(_wheel_text(), encoding="utf-8")
    (dist_info / "entry_points.txt").write_text(_entry_points_text(), encoding="utf-8")
    (dist_info / "top_level.txt").write_text(_top_level_text(), encoding="utf-8")
    return dist_info


def get_requires_for_build_wheel(config_settings=None):
    return []


def get_requires_for_build_sdist(config_settings=None):
    return []


def prepare_metadata_for_build_wheel(metadata_directory, config_settings=None):
    _write_metadata_dir(metadata_directory)
    return DIST_INFO


def build_wheel(wheel_directory, config_settings=None, metadata_directory=None):
    wheel_directory = Path(wheel_directory)
    wheel_directory.mkdir(parents=True, exist_ok=True)
    wheel_path = wheel_directory / WHEEL_NAME

    records: list[tuple[str, str, str]] = []

    def add_bytes(zf: zipfile.ZipFile, arcname: str, data: bytes) -> None:
        zf.writestr(arcname, data)
        records.append((arcname, _hash_bytes(data), str(len(data))))

    with tempfile.TemporaryDirectory() as tmpdir:
        dist_info = _write_metadata_dir(tmpdir)

        with zipfile.ZipFile(wheel_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
            for path in _package_files():
                arcname = path.relative_to(_project_root()).as_posix()
                data = path.read_bytes()
                add_bytes(zf, arcname, data)

            for filename in ["METADATA", "WHEEL", "entry_points.txt", "top_level.txt"]:
                path = dist_info / filename
                arcname = f"{DIST_INFO}/{filename}"
                data = path.read_bytes()
                add_bytes(zf, arcname, data)

            record_rows = records + [(f"{DIST_INFO}/RECORD", "", "")]
            record_text = "\n".join(
                ",".join(row) for row in record_rows
            ) + "\n"
            zf.writestr(f"{DIST_INFO}/RECORD", record_text.encode("utf-8"))

    return wheel_path.name


def build_sdist(sdist_directory, config_settings=None):
    sdist_directory = Path(sdist_directory)
    sdist_directory.mkdir(parents=True, exist_ok=True)
    archive_name = f"{NAME}-{VERSION}.tar.gz"
    archive_path = sdist_directory / archive_name

    import tarfile

    with tarfile.open(archive_path, "w:gz") as tf:
        root = _project_root()
        for path in _package_files():
            arcname = f"{NAME}-{VERSION}/{path.relative_to(root).as_posix()}"
            tf.add(path, arcname=arcname)

        for extra in ["README.md", "LICENSE", "pyproject.toml", "build_backend.py", "requirements.txt"]:
            path = root / extra
            if path.exists():
                tf.add(path, arcname=f"{NAME}-{VERSION}/{extra}")

    return archive_name
