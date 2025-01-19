from rich import print

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.markdown import Markdown

def help():
    return

def print_short(result):
    console = Console()
    description_text = Text("Description: ", style="bold green") + Text(result['description'], style="yellow")
    markdown_block = Markdown(f"```{result['type']}\n{result['syntax']}\n```")
    stx_text = Text("Syntax: ", style="bold green")
    console.print(stx_text)
    console.print(markdown_block)
    console.print(description_text)

def print_to_terminal(result):
    console = Console()

    # Custom rich formatting for each part
    command_text = Text("Command: ", style="bold green") + Text(result['command'], style="cyan")
    type_text = Text("Type: ", style="bold green") + Text(result['type'], style="magenta")
    description_text = Text("Description: ", style="bold green") + Text(result['description'], style="yellow")
    syntax_text = Text("Syntax: ", style="bold green") + Text(result['syntax'], style="cyan")
    usage_text = Text("Usage: ", style="bold green") + Text(result['usage'], style="cyan")
    params_text = Text("Parameters: ", style="bold green")
    stx_text = Text("Syntax: ", style="bold green")
    for param in result['params']:
        params_text.append(f"\n  - {param}", style="white")

    # Generate a Markdown code block for the syntax
    markdown_block = Markdown(f"```{result['type']}\n{result['syntax']}\n```")

    console.print(command_text)
    console.print(type_text)
    console.print(description_text)
    console.print(stx_text)
    console.print(markdown_block)
    console.print(Panel(usage_text, title="Usage", border_style="cyan"))
    console.print(Panel(params_text, title="Parameters", border_style="green"))


def display_help():
    console = Console()

    console.print("[bold cyan]MyCLI Tool[/bold cyan] - A CLI tool for amazing tasks\n")

    console.print("Usage:")
    console.print("  [bold]mycli [command] [options][/bold]\n")

    console.print("Commands:")
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Command", style="cyan", no_wrap=True)
    table.add_column("Description", style="green")
    table.add_column("Example", style="yellow")

    table.add_row(
        "init",
        "Initialize the project in the current directory",
        "mycli init"
    )
    table.add_row(
        "add",
        "Add a new item to the project",
        "mycli add --name 'ItemName'"
    )
    table.add_row(
        "remove",
        "Remove an item from the project",
        "mycli remove --id 123"
    )
    table.add_row(
        "list",
        "List all items in the project",
        "mycli list --all"
    )

    console.print(table)

    console.print("\nOptions:")
    console.print("  [bold]--help[/bold]       Show this help message and exit")
    console.print("  [bold]--version[/bold]    Show the version of the tool\n")

    console.print(Text("For more details, visit: ", style="dim") + Text("https://example.com/docs",
                                                                        style="link https://example.com/docs"))

# [flags] [query] [n_results]
def parse_args(args):
    parsing_flags = True
    flags = []
    query = ""
    n_results = 1
    
    if args[-1].isdigit():
        n_results = int(args[-1])
        args = args[:-1]

    for arg in args:
        if parsing_flags:
            if arg[0] != '-':
                parsing_flags = False
            else:
                validate_flag(arg)
                flags.append(arg)
        
        if not parsing_flags:
            query += arg + " "

    if not query:
        raise Exception("Query cannot be empty")
    return flags, query, n_results

def validate_flag(flag):
    valid_flags = ['-ai', '-v']
    if flag not in valid_flags:
        raise Exception("Invalid flag parameter")