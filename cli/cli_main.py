from rich import print
from query import man_search, vec_search
from cli.cli_helpers import parse_args, print_to_terminal

def run_cli(args, json_objects_dict, db):
    if args[0].lower() == "help":
        return help()
    
    try: 
        flags, query, n_results = parse_args(args)

        if not flags or '-ai' not in flags:
            result = man_search(query, json_objects_dict)
        else:
            result = vec_search(query, n_results, db)

        print_to_terminal(result)

    except Exception as e:
        print(f"[bold red]Invalid arguments:[/bold red] {e}")