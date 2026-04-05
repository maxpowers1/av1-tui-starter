"""Entry point for av1-tui."""

from av1_tui.app import Av1TuiApp


def main() -> None:
    app = Av1TuiApp()
    app.run()


if __name__ == "__main__":
    main()
