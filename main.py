import ui.searchPage
import sys
import chromadb
from backend.data_parser import parse_json
from backend.json_to_chromaDB import insert_to_chroma
from cli.cli_main import run_cli

chroma_client = chromadb.Client()
db = chroma_client.create_collection(name="my_collection")

json_objects_dict = parse_json()

insert_to_chroma(json_objects_dict, db)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        args = sys.argv[1:]
        run_cli(args, json_objects_dict, db)
    else:
        app = ui.searchPage.SearchBarApp()
        app.run()
        print(2)
