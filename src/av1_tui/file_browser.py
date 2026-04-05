"""File browser screen for selecting video files."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

from textual import on
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import (
    DirectoryTree,
    Footer,
    Header,
    Label,
    ListView,
    ListItem,
    Static,
)


VIDEO_EXTENSIONS: frozenset[str] = frozenset(
    {
        ".mp4",
        ".mkv",
        ".avi",
        ".mov",
        ".wmv",
        ".flv",
        ".webm",
        ".m4v",
        ".mpg",
        ".mpeg",
        ".ts",
        ".vob",
        ".3gp",
    }
)


def is_video_file(path: Path) -> bool:
    """Check if a path is a video file based on its extension."""
    return path.is_file() and path.suffix.lower() in VIDEO_EXTENSIONS


class VideoDirectoryTree(DirectoryTree):
    """A directory tree that only shows directories and video files."""

    def filter_paths(self, paths: Iterable[Path]) -> Iterable[Path]:
        return [path for path in paths if path.is_dir() or is_video_file(path)]


class FileBrowserScreen(Screen):
    """Screen for browsing and selecting video files."""

    BINDINGS = [
        Binding("space", "toggle_select", "Toggle select"),
        Binding("a", "select_all", "Select all visible"),
        Binding("c", "clear_selection", "Clear selection"),
        Binding("enter", "confirm", "Confirm"),
        Binding("q", "app.quit", "Quit"),
    ]

    CSS = """
    #browser-layout {
        layout: horizontal;
    }

    #tree-panel {
        width: 2fr;
        height: 100%;
    }

    #instructions {
        padding: 1;
        background: $surface;
        color: $text-muted;
        dock: top;
    }

    #selection-panel {
        width: 1fr;
        height: 100%;
        border-left: solid $accent;
        padding: 0 1;
    }

    #selection-header {
        text-style: bold;
        padding: 0 0 1 0;
    }

    #selection-list {
        height: 1fr;
    }

    #selection-empty {
        color: $text-disabled;
        padding: 1 0;
    }

    #selection-count {
        dock: bottom;
        padding: 1 0 0 0;
        text-style: italic;
    }
    """

    def __init__(self, start_path: Path | None = None) -> None:
        super().__init__()
        self._start_path = start_path or Path.home()
        self._selected: dict[Path, ListItem] = {}

    @property
    def selected_files(self) -> list[Path]:
        """Return the list of currently selected file paths."""
        return list(self._selected.keys())

    INSTRUCTIONS = (
        "Navigate the tree to find video files. "
        "Press [b]Space[/b] to toggle a file, "
        "[b]A[/b] to select all visible, "
        "[b]C[/b] to clear selection, "
        "[b]Enter[/b] to confirm."
    )

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static(self.INSTRUCTIONS, id="instructions", markup=True)
        with Horizontal(id="browser-layout"):
            with Vertical(id="tree-panel"):
                yield VideoDirectoryTree(self._start_path)
            with Vertical(id="selection-panel"):
                yield Static("Selected Files", id="selection-header")
                yield Static(
                    "No files selected yet",
                    id="selection-empty",
                )
                yield ListView(id="selection-list")
                yield Label("0 files selected", id="selection-count")
        yield Footer()

    @on(DirectoryTree.FileSelected)
    def on_file_selected(self, event: DirectoryTree.FileSelected) -> None:
        """Toggle selection when a file is clicked."""
        self._toggle_path(event.path)

    def action_toggle_select(self) -> None:
        """Toggle the currently highlighted file."""
        tree = self.query_one(VideoDirectoryTree)
        node = tree.cursor_node
        if node is None:
            return
        path = node.data.path if node.data else None
        if path and is_video_file(path):
            self._toggle_path(path)

    def action_select_all(self) -> None:
        """Select all visible video files in the currently expanded tree."""
        tree = self.query_one(VideoDirectoryTree)
        # Walk only the visible (expanded) portion of the tree
        stack = [tree.root]
        while stack:
            node = stack.pop()
            if node.data and hasattr(node.data, "path"):
                path = node.data.path
                if is_video_file(path) and path not in self._selected:
                    self._add_to_selection(path)
            if node.is_expanded:
                stack.extend(node.children)

    def action_clear_selection(self) -> None:
        """Clear all selected files."""
        selection_list = self.query_one("#selection-list", ListView)
        selection_list.clear()
        self._selected.clear()
        self._update_status()

    def action_confirm(self) -> None:
        """Confirm the selection and proceed."""
        if self._selected:
            self.dismiss(self.selected_files)

    def _toggle_path(self, path: Path) -> None:
        if path in self._selected:
            self._remove_from_selection(path)
        else:
            self._add_to_selection(path)

    def _add_to_selection(self, path: Path) -> None:
        selection_list = self.query_one("#selection-list", ListView)
        try:
            display = str(path.relative_to(self._start_path))
        except ValueError:
            display = path.name
        item = ListItem(Label(display))
        self._selected[path] = item
        selection_list.append(item)
        self._update_status()

    def _remove_from_selection(self, path: Path) -> None:
        item = self._selected.pop(path, None)
        if item is not None:
            item.remove()
        self._update_status()

    def _update_status(self) -> None:
        count = len(self._selected)
        label = self.query_one("#selection-count", Label)
        label.update(f"{count} file{'s' if count != 1 else ''} selected")
        empty_hint = self.query_one("#selection-empty", Static)
        empty_hint.display = count == 0
