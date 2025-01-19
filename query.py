def man_search(command, db):
    for id in db:
        if db[id]['command'] == command:
            return [db[id]]
    return None

def vec_search(query, n_results, db):
    results = db.query(query_texts=[query], n_results=n_results)
    return results['ids'][0]