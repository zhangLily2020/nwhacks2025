from textual.app import App
from textual.containers import Horizontal, Vertical
from textual.widgets import Input, ListView, ListItem, Label
from textual.screen import Screen


class TelescopeView(Screen):
    def compose(self):
        # Main layout container
        with Horizontal():
            # Left section: Search bar and file selector
            with Vertical():
                # Search bar
                yield Label("Search", id="search-label")
                yield Input(placeholder="Type to search...", id="search-bar")

                # File selector
                yield Label("Files", id="file-label")
                yield ListView(
                    ListItem(Label("File 1")),
                    ListItem(Label("File 2")),
                    ListItem(Label("File 3")),
                    id="file-selector",
                )

            # Right section: Info page
            with Vertical():
                yield Label("Info Panel", id="info-label")
                yield Label("Select a file to view details here.", id="info-content")


class TelescopeApp(App):
    def on_mount(self):
        self.push_screen(TelescopeView())


if __name__ == "__main__":
    app = TelescopeApp()
    app.run()
