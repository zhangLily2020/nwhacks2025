from rich import print
from query import man_search, vec_search
from cli.cli_helpers import parse_args, print_to_terminal, print_short, display_help
import chromadb
from backend.json_to_chromaDB import insert_to_chroma

def CreateChroma(json_objects_dict):
    chroma_client = chromadb.PersistentClient(path='../backend')
    db = chroma_client.get_or_create_collection(name="manpp")
    return chroma_client, db

def run_cli(args, json_objects_dict):
    if args[0].lower() == "help":
        return display_help()
    
    try: 
        flags, query, n_results = parse_args(args)

        if not flags or '-vec' not in flags:
            result = man_search(query, json_objects_dict)
        else:
            chroma_client, db = CreateChroma(json_objects_dict)
            result = vec_search(query, n_results, db)
        if not flags or '-v' not in flags:
            for r in result:
                print_short(json_objects_dict[int(r)])
        else:
            for r in result:
                print_to_terminal(json_objects_dict[int(r)])

    except Exception as e:
        print(f"[bold red]Invalid arguments:[/bold red] {e}")