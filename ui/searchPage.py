from textual.app import App, ComposeResult
from textual.containers import Container, VerticalScroll
from textual.widgets import Input, Button, Select, Static, Footer, Header
from textual.fuzzy import FuzzySearch

class SearchBarApp(App):
    CSS_PATH = "searchPage.tcss"

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

    async def on_input_changed(self, event: Input.Changed) -> None:
        """Handle input changes dynamically."""
        search_input = event.value.strip()  # Get current input
        search_type = self.query_one("#search_type", Select).value
        output_widget = self.query_one("#output", Static)

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

            # Display results
            if results:
                output_text = "Fuzzy Search Results:\n"
                for result, score in results:
                    output_text += f"- {result} (Score: {score:.2f})\n"
            else:
                output_text = "No matches found."
        else:
            output_text = ""

        # Update the output widget
        output_widget.update(output_text)
        output_widget.add_class("styled")


if __name__ == "__main__":
    app = SearchBarApp()
    app.run()
