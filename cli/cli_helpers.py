from rich import print

def help():
    return

def print_to_terminal(result):
    print(result)

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
    valid_flags = ['-ai']
    if flag not in valid_flags:
        raise Exception("Invalid flag parameter")