from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical, VerticalScroll, Container
from textual.widgets import Input, Button, Select, Footer, Header, ListView, ListItem, Label
from textual.screen import Screen
from textual.fuzzy import FuzzySearch

def CreateCandidates(dict, cmd_to_idx):
    res = []
    for key in dict:
        res.append(dict[key]['command'])
        cmd_to_idx[dict[key]['command']] = key
    return res

class TelescopeView(Screen):
    CSS_PATH = "telescope.tcss"

    def __init__(self, db, input_dict) -> None:
        super().__init__()
        self.db = db
        self.input_dict = input_dict
        self.cmd_to_idx = {}
        self.my_query = ""
        self.candidates = CreateCandidates(input_dict, self.cmd_to_idx)

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
                self.info_name = Label("Info Panel", id="info-label")
                self.info_content = Label("Select a file to view details here.", id="info-content")
                yield self.info_name
                yield self.info_content

        yield Footer()
        yield Header(show_clock=True)

    async def on_input_changed(self, event: Input.Changed) -> None:
        """Handle input changes dynamically."""
        search_input = event.value.strip()  # Get current input
        search_type = self.query_one("#search_type", Select).value
        output_container = self.query_one("#output_container", ListView)

        # Sample data for fuzzy search
        candidates = self.candidates

        if search_type == "vector" and search_input:
            self.my_query = search_input

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
            if results:
                for result, score in results:
                    idx = self.cmd_to_idx[result]
                    await output_container.append(
                        ListItem(Label(f"{result}"), id="a" + str(idx))
                    )
            else:
                await output_container.append(ListItem(Label("No matches found.")))
        else:
            await output_container.clear()
            await output_container.append(ListItem(Label("No input or invalid search type.")))

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        output_container = self.query_one("#output_container", ListView)
        if event.button.id == "search_button":
            search_input = self.query_one("#search_input", Input).value.strip()
            search_type = self.query_one("#search_type", Select).value

            if search_type == "vector" and search_input:
                await output_container.clear()

                results = self.db.query(query_texts=[self.my_query], n_results=8)['ids'][0]
                for str_idx in results:
                    idx = int(str_idx)
                    new_res = self.input_dict[idx]
                    await output_container.append(ListItem(Label(f"{new_res['command']}"), id="a" + str(idx)))


    def on_list_view_selected(self, event: ListView.Selected):
            """Handle selection of items in the file selector."""
            selected_item = event.item
            if selected_item:
                idx = int(selected_item.id[1:])
                cmd = self.input_dict[idx]
                self.info_name.update(f"Name: {cmd['command']}")
                self.info_content.update(f"Description: {cmd['description']}")


    def do_vec_search(self):
        results = self.db.query(query_texts=[""], n_results=1)

class TelescopeApp(App):
    def __init__(self, db, input_dict) -> None:
        super().__init__()
        self.db = db
        self.input_dict = input_dict

    def on_mount(self) -> None:
        self.theme = "gruvbox"
        self.push_screen(TelescopeView(db=self.db, input_dict=self.input_dict))


if __name__ == "__main__":
    app = TelescopeApp()
    app.run()