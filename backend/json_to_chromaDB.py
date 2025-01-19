def insert_to_chroma(dict, db):
    id_strings = []
    docs = []
    for id in dict:
        id_strings.append(str(id))
        command = dict[id]
        docs.append(f"[{command['type']}] {command['description']}")
    db.add(
        documents=docs,
        ids=id_strings
    )