from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import Footer, Label

from .cli import main as cli_main


class BeepyWebRadioApp(App):
    BINDINGS = [
        Binding("q", "quit", "Quit", show=True),
    ]

    def compose(self) -> ComposeResult:
        yield Label("Beepy Web Radio")
        yield Footer()

    def on_mount(self) -> None:
        pass


def main() -> None:
    import sys

    if len(sys.argv) > 1:
        cli_main()
    else:
        BeepyWebRadioApp().run()


if __name__ == "__main__":
    main()
