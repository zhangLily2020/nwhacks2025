import chromadb
from backend.data_parser import parse_json
from backend.json_to_chromaDB import insert_to_chroma



def CreateVecDatabase(path):
    # Initialize ChromaDB with persistence
    client = chromadb.PersistentClient(path=path)

    json_objects_dict = parse_json()

    # Create or load a collection
    db = client.get_or_create_collection("manpp")

    # Add documents (only the first time; they will persist afterward)
    insert_to_chroma(json_objects_dict, db)