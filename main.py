import ui.searchPage
import ui.telescope
import sys
import chromadb
from backend.data_parser import parse_json
from backend.json_to_chromaDB import insert_to_chroma
from cli.cli_main import run_cli
from backend.create_db import CreateVecDatabase
import chromadb.config
import os

def CreateChroma(json_objects_dict):
    chroma_client = chromadb.PersistentClient(path="./backend")
    db = chroma_client.get_or_create_collection(name="manpp")
    return chroma_client, db

json_objects_dict = parse_json()

def CreateChromaIfNotExist(directory: str, filename: str):
    file_path = os.path.join(directory, filename)
    if not os.path.isfile(file_path):
        CreateVecDatabase('./backend')
        return True
    return False

if __name__ == '__main__':
    CreateChromaIfNotExist('./backend', 'chroma.sqlite3')

    if len(sys.argv) > 1:
        args = sys.argv[1:]
        run_cli(args, json_objects_dict)
    else:
        chroma_client, db = CreateChroma(json_objects_dict)
        # app = ui.searchPage.SearchBarApp()
        app = ui.telescope.TelescopeApp()
        app.run()
        print(2)
