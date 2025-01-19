from textual.app import App, ComposeResult
from textual.containers import Container, VerticalScroll
from textual.widgets import Input, Button, Select, Static, RadioSet, RadioButton, Footer, Header


class SearchBarApp(App):
    CSS_PATH = "searchPage.tcss"
    # def on_mount(self) -> None:
    #     self.theme = "solarized-light"

    def on_mount(self) -> None:
        self.title = "Man++"

    def compose(self) -> ComposeResult:
        """Create the widgets for the UI."""
        with Container():
            yield Input(placeholder="Search here...", id="search_input")
            yield Select(
                options=[("Fuzzy Search", "fuzzy"), ("Vector Search", "vector")],
                id="search_type"
            )
            yield Button("🔍", id="search_button")
        yield VerticalScroll(Static("", id="output"))  # To display search results
        yield Footer()
        yield Header(show_clock=True)

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        if event.button.id == "search_button":
            search_input = self.query_one("#search_input", Input).value
            search_type = self.query_one("#search_type", Select).value
            output_widget = self.query_one("#output", Static)

            #send and receive query
            returned_values = []

            #temp
            x = '''{
                  "command": "git init",
                  "type": "git",
                  "description": "Initializes a new Git repository.",
                  "syntax": "git init [DIRECTORY]",
                  "usage": "git init my-project",
                  "params": [
                    "--bare: Create a bare repository (no working directory).",
                    "-q: Suppress output."
                  ]
                }'''
            returned_values.append(x)

            if search_type in ["fuzzy", "vector"]:
                search_type_display = search_type.capitalize()  # Show "Fuzzy" or "Vector"
            else:
                search_type_display = "Not Selected"

            # Display the selected option and search query
            output_widget.update(f"Search type: {search_type_display}\nQuery Results: {x}")
            output_widget.add_class("styled")

    def action_add_radio_buttons(self) -> None:
        """Add more RadioButtons to the RadioSet."""
        radio_set = self.query_one("#radio_set")
        radio_set.mount(RadioButton("New RadioButton"))

if __name__ == "__main__":
    app = SearchBarApp()
    app.run()
