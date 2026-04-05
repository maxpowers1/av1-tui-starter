"""Textual application shell."""

from textual.app import App


class Av1TuiApp(App):
    """AV1 encoding TUI application."""

    TITLE = "av1-tui"

    def compose(self):
        yield from []  # screens added in later commits
