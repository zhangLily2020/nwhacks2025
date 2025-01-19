from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical, VerticalScroll
# from textual.app import App, ComposeResult
# from textual.containers import Container, VerticalScroll
# from textual.widgets import Input, ListView, ListItem, Label
from textual.widgets import (Input, Button, Select, Checkbox, Footer, Header, RadioButton, RadioSet,
                             ListView, ListItem, Label)
from textual.screen import Screen
from textual.fuzzy import FuzzySearch


class TelescopeView(Screen):
    CSS_PATH = "telescope.tcss"
    def compose(self):
        # Main layout container
        with Horizontal():
            # Left section: Search bar and file selector
            with Vertical():
                # # Search bar
                # yield Label("Search", id="search-label")
                # yield Input(placeholder="Type to search...", id="search-bar")
                #
                # # File selector
                # yield Label("Files", id="file-label")
                # yield ListView(
                #     ListItem(Label("File 1")),
                #     ListItem(Label("File 2")),
                #     ListItem(Label("File 3")),
                #     id="file-selector",
                # )
                with Container():
                    yield Input(placeholder="Search here...", id="search_input")
                    yield Select(
                        options=[("Fuzzy Search", "fuzzy"), ("Vector Search", "vector")],
                        id="search_type"
                    )
                    yield Button("🔍", id="search_button")
                yield VerticalScroll(RadioSet(id="output_container"))  # Container for Checkboxes

            # Right section: Info page
            with Vertical():
                yield Label("Info Panel", id="info-label")
                yield Label("Select a file to view details here.", id="info-content")

        yield Footer()
        yield Header(show_clock=True)

    async def on_input_changed(self, event: Input.Changed) -> None:
        """Handle input changes dynamically."""
        search_input = event.value.strip()  # Get current input
        search_type = self.query_one("#search_type", Select).value
        output_container = self.query_one("#output_container", RadioSet)

        # Sample data for fuzzy search
        candidates = [
            "git init",
            "git commit",
            "git push origin main",
            "git clone https://example.com/repo.git",
            "git status",
            "git log --oneline",
            "git pull",
        ]

        if search_type == "fuzzy" and search_input:
            # Perform fuzzy search
            searcher = FuzzySearch()
            results = [
                (candidate, score)
                for candidate in candidates
                if (score := searcher.match(search_input, candidate)[0]) > 0
            ]

            # Sort by score (higher is better)
            results.sort(key=lambda x: x[1], reverse=True)

            # Clear previous results
            await output_container.remove_children()

            # Add new results as Checkboxes
            if results:
                for result, score in results:
                    await output_container.mount(
                        RadioButton(f"{result} (Score: {score:.2f})", value=False)
                    )
            else:
                await output_container.mount(RadioButton("No matches found.", value=False))
        else:
            await output_container.remove_children()
            await output_container.mount(RadioButton("No input or invalid search type.", value=False))


class TelescopeApp(App):
    def on_mount(self):
        self.push_screen(TelescopeView())


if __name__ == "__main__":
    app = TelescopeApp()
    app.run()
