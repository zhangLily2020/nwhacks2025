import rich.syntax
from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical, VerticalScroll, Container
from textual.widgets import Input, Button, Select, Footer, Header, ListView, ListItem, Label, LoadingIndicator, Markdown, Static
from textual.screen import Screen
from textual.fuzzy import FuzzySearch
from rich.text import Text
from rich.console import Group
from rich_pixels import Pixels
from rich.columns import Columns
from rich.layout import Layout
from rich.panel import Panel
from rich import box

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
                        id="search_type",
                        value="fuzzy"
                    )
                    yield Button("🔍", id="search_button")
                yield VerticalScroll(ListView(id="output_container"))  # Container for search results

            # Right section: Info page
            with VerticalScroll(id="vertical"):
                # Create the text panel
                txt = Text("Go and start searching >v<")
                panel = Panel(txt, title="termiknow", height=5)  # Adjust height as needed
                pixels = Pixels.from_image_path("ui/logo_small.png")
                pixels_panel = Panel(pixels, height=13, box=box.SIMPLE)  # Match the height

                layout = Layout(size=15)
                layout.split_row(
                    Layout(panel, ratio=1, name="panel"),
                    Layout(pixels_panel, ratio=1, name="image")
                )

                self.title_view = Static(layout, id="horizontal_title")
                yield self.title_view

                self.info_content = Static("", id="info-content")
                # Rich Text for the description
                self.desc = Static("", id="info-desc")

                # Syntax using Markdown for formatting (optional)
                self.syntax = Static("", id="info-syntax")
                # self.syntax.add_class("no_bg")

                self.usage = Markdown("", id="info-usage")
                self.usage.add_class("no_bg")

                # Parameters using Markdown
                self.params = Markdown("", id="info-params")
                self.params.add_class("no_bg")


                yield self.info_content
                yield self.desc
                yield self.usage
                yield self.syntax
                yield self.params

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
            output_container.refresh(layout=True)
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
                await output_container.append(ListItem(Label("No matches found."), id="nothing"))
        else:
            await output_container.clear()
            await output_container.append(ListItem(Label("No input or invalid search type."), id="nothing"))



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
            if selected_item.id == "nothing":
                return

            idx = int(selected_item.id[1:])
            cmd = self.input_dict[idx]

            # Create the text panel
            txt = Text(f"{cmd['command']}")
            panel = Panel(txt, title="termiknow", height=5)  # Adjust height as needed
            pixels = Pixels.from_image_path("ui/logo_small.png")
            pixels_panel = Panel(pixels, height=13, box=box.SIMPLE)  # Match the height

            layout = Layout(size=15)
            layout.split_row(
                Layout(panel, ratio=1, name="panel"),
                Layout(pixels_panel, ratio=1, name="image")
            )
            self.title_view.update(layout)


            rich_text_type = Text("Type: ", style="bold blue") + Text(cmd['type'], style="yellow")
            self.info_content.update(rich_text_type)

            # Update description
            rich_text_desc = Text("Description: ", style="bold magenta") + Text(cmd['description'], style="white")
            self.desc.update(rich_text_desc)

            # Update
            syntax_label = Text("Usage:", style="bold")  # Add label above syntax
            rich_syntax = rich.syntax.Syntax(cmd['usage'], cmd['type'], line_numbers=True)
            # Combine label and syntax using a Vertical Static or similar container
            syntax_combined = Group(syntax_label, rich_syntax)
            self.syntax.update(syntax_combined)
            # self.syntax.remove_class("no_bg")
            # self.syntax.add_class('place_bg')

            # Update usage
            self.usage.update(f"**Syntax:**\n```{cmd['type']}\n{cmd['syntax']}\n```")
            self.usage.remove_class("no_bg")
            self.usage.add_class('place_bg')

            # Update parameters
            params_md = "\n".join(f"- {param}" for param in cmd['params'])
            self.params.update(f"**Parameters:**\n{params_md}")
            self.params.remove_class("no_bg")
            self.params.add_class('place_bg')

class TelescopeApp(App):
    def __init__(self, db, input_dict) -> None:
        super().__init__()
        self.db = db
        self.input_dict = input_dict

    def on_mount(self) -> None:
        self.theme = "gruvbox"
        self.push_screen(TelescopeView(db=self.db, input_dict=self.input_dict))
        self.title = "termiknow"


if __name__ == "__main__":
    app = TelescopeApp()
    app.run()