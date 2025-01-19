def man_search(command, dict):
    command = command.strip()
    for id in dict:
        tmp = dict[id]['command'].strip()
        if tmp == command:
            return [id]
    raise Exception("Command doesn't exist")

def vec_search(query, n_results, db):
    results = db.query(query_texts=[query], n_results=n_results)
    print(results)
    return results['ids'][0]