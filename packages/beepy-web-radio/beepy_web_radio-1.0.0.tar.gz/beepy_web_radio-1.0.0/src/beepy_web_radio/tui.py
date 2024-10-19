import logging

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import Footer, Input, Label, ListItem, ListView, Static

from beepy_web_radio.api import get_stations, play_station, stop_playback

# Set up logging
logging.basicConfig(
    filename="/tmp/beepy_web_radio.log",
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


class BeepyWebRadioApp(App):
    BINDINGS = [
        Binding("q", "quit", "Quit", show=True),
        Binding("s", "stop", "Stop Playback", show=True),
        Binding("j", "stop", "Down", show=True),
        Binding("k", "stop", "Up", show=True),
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logger = logger

    def compose(self) -> ComposeResult:
        self.logger.info("Composing BeepyWebRadioApp")
        yield Static("Beepy Web Radio", id="title")
        yield Input(
            placeholder="Search for stations... (Press Enter to search)",
            id="search",
        )
        yield ListView(id="stations")
        yield Static(id="now_playing")
        yield Footer()

    def on_mount(self) -> None:
        self.logger.info("BeepyWebRadioApp mounted")
        self.query_one("#search").focus()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        if event.input.id == "search":
            self.logger.info(f"Search submitted: {event.value}")
            self.search_stations(event.value)

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        station = str(event.item.get_child_by_type(Label).renderable)
        self.logger.info(f"Station selected: {station}")
        self.play_station(station)

    def search_stations(self, query: str) -> None:
        self.logger.info(f"Searching stations with query: {query}")
        stations = get_stations(query)
        self.logger.info(f"Found {len(stations)} stations")
        self.logger.info(stations)
        list_view = self.query_one("#stations")
        list_view.clear()
        for station in stations:
            list_view.append(ListItem(Label(station["title"])))

    def play_station(self, station: str) -> None:
        self.logger.info(f"Playing station: {station}")
        play_station(station)
        self.query_one("#now_playing").update(f"Now playing: {station}")

    def action_stop(self) -> None:
        self.logger.info("Stopping playback")
        stop_playback()
        self.query_one("#now_playing").update("Playback stopped")

    def action_quit(self) -> None:
        self.logger.info("Quitting application")
        self.exit()
