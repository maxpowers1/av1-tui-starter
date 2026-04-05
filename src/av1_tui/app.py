"""Textual application shell."""

from __future__ import annotations

from pathlib import Path

from textual.app import App

from av1_tui.file_browser import FileBrowserScreen


class Av1TuiApp(App):
    """AV1 encoding TUI application."""

    TITLE = "av1-tui"

    def on_mount(self) -> None:
        self.push_screen(FileBrowserScreen(), callback=self._on_files_selected)

    def _on_files_selected(self, files: list[Path]) -> None:
        """Handle confirmed file selection."""
        # Next step: push encoding config screen with these files
        self.exit(files)
