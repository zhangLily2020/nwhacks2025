from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical, VerticalScroll, Container
from textual.widgets import Input, Button, Select, Footer, Header, ListView, ListItem, Label
from textual.screen import Screen
from textual.fuzzy import FuzzySearch

class TelescopeView(Screen):
    CSS_PATH = "telescope.tcss"

    def compose(self) -> ComposeResult:
        # Main layout container
        with Horizontal():
            # Left section: Search bar and file selector
            with Vertical():
                with Container():
                    yield Input(placeholder="Search here...", id="search_input")
                    yield Select(
                        options=[("Fuzzy", "fuzzy"), ("Vector", "vector")],
                        id="search_type"
                    )
                    yield Button("🔍", id="search_button")
                yield VerticalScroll(ListView(id="output_container"))  # Container for search results

            # Right section: Info page
            with Vertical():
                yield Label("Info Panel", id="info-label")
                self.info_content = Label("Select a file to view details here.", id="info-content")
                yield self.info_content
        yield Footer()
        yield Header(show_clock=True)

    async def on_input_changed(self, event: Input.Changed) -> None:
        """Handle input changes dynamically."""
        search_input = event.value.strip()  # Get current input
        search_type = self.query_one("#search_type", Select).value
        output_container = self.query_one("#output_container", ListView)

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
            await output_container.clear()

            # Add new results as ListItems
            x = 0
            if results:
                for result, score in results:
                    await output_container.append(
                        ListItem(Label(f"{result}"), id="a" + str(x))
                    )
                    x += 1
            else:
                await output_container.append(ListItem(Label("No matches found.")))
        else:
            await output_container.clear()
            await output_container.append(ListItem(Label("No input or invalid search type.")))

    def on_list_view_selected(self, event: ListView.Selected):
            """Handle selection of items in the file selector."""
            selected_item = event.item
            if selected_item:
                self.info_content.update(f"Selected: {selected_item.id}")

class TelescopeApp(App):
    def on_mount(self) -> None:
        self.theme = "gruvbox"
        self.push_screen(TelescopeView())


if __name__ == "__main__":
    app = TelescopeApp()
    app.run()
