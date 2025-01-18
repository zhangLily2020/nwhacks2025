from textual.app import App, ComposeResult
from textual.containers import Container
from textual.widgets import Input, Button, Select, Static

class SearchBarApp(App):
    CSS = """
    Screen {
        align: center middle;
        padding: 2;
        # background: #f0f0f0;
    }

    Container {
        width: 70%;
        height: 5;
        layout: horizontal;
        align: center middle;
        border: round #cccccc;
        # background: white;
    }

    Input {
        width: 60%;
        height: auto;
        padding: 1;
        # border: white;
    }

    Select {
        width: 25%;
        height: auto;
        align: center middle;
    }

    Button {
        width: 15%;
        align: center middle;
        background: #4285f4;
        color: white;
        border: none;
        height: auto;
        padding: 1;
    }

    Button:hover {
        background: #357ae8;
    }

    #output {
        margin-top: 1;
        color: black;
    }
    """

    def compose(self) -> ComposeResult:
        """Create the widgets for the UI."""
        with Container():
            yield Input(placeholder="Search here...", id="search_input")
            yield Select(
                options=[("Fuzzy Search", "fuzzy"), ("Vector Search", "vector")],
                id="search_type"
            )
            yield Button("Search", id="search_button")
        yield Static("", id="output")  # To display search results

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        if event.button.id == "search_button":
            search_input = self.query_one("#search_input", Input).value
            search_type = self.query_one("#search_type", Select).value
            output_widget = self.query_one("#output", Static)

            # Display the selected option and search query
            output_widget.update(f"Search type: {search_type}\nQuery: {search_input}")

if __name__ == "__main__":
    app = SearchBarApp()
    app.run()
