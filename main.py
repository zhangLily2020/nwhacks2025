import ui.searchPage
import sys
from backend.data_parser import parse_json
from backend.json_to_chromaDB import insert_to_chroma
from cli.cli_main import run_cli

json_objects_dict = parse_json()
db = None #initialize
insert_to_chroma(json_objects_dict, db)

if __name__ == '__main__':
    print(sys.argv)
    if len(sys.argv) > 1:
        args = sys.argv[1:]
        run_cli(args, db)
    else:
        #app = ui.searchPage.SearchBarApp()
        # app.run()
        print(2)
