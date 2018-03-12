import re
import itertools
import json
import sys

# tokens
def tokenize(text):
    alphanumeric = "[a-zA-Z][a-zA-Z0-9]+"
    table_name = alphanumeric + "\." + alphanumeric
    open_parens = "\("
    close_parens = "\)"
    comma = ","
    semicolon = ";"
    comment1 = "--.*\n"
    comment2 = "--.*$"
    possible_tokens = [comment1, comment2, table_name, alphanumeric, open_parens, close_parens, comma, semicolon]
    token_regex = "(" + "|".join(possible_tokens) + ")"
    known_keywords = [
        "CREATE", "SCHEMA", "TABLE", "INTEGER", "BOOLEAN", "NOT", "NULL",
        "TEXT", "DEFAULT", "TIMESTAMP", "WITH", "TIME", "ZONE"
    ]
    tokens = re.findall(token_regex, text)
    def normalize(x):
        if x.upper() in known_keywords:
            return x.upper()
        elif x.startswith("--"):
            return "COMMENT"
        else:
            return x
    return [normalize(x) for x in tokens]

def starts(line, start):
    try:
        for (i, x) in enumerate(start):
            if x != line[i]:
                return False
        else:
            return True
    except IndexError:
        return False

def contains(line, c):
    if not line:
        return False
    if starts(line, c):
        return True
    else:
        return contains(line[1:], c)

def split_by(separator, tokens):
    res = []
    curr = []
    for i in tokens:
        if i == separator:
            res.append(curr)
            curr = []
        else:
            curr.append(i)
    if curr:
        res.append(curr)
    return res
        
def parse(text):
    res = {}
    tokens = [x for x in tokenize(text) if x != "COMMENT"]
    for line in split_by(";", tokens):
        if starts(line, ["CREATE", "SCHEMA"]):
            res[line[2]] = {}
        elif starts(line, ["CREATE", "TABLE"]):
            schema, table = line[2].split(".")
            res[schema][table] = parse_table(line[3:])
    return res

def parse_table(tabledef):
    if tabledef[0] != "(" or tabledef[-1] != ")":
        raise Exception("Invalid table syntax")
    res = {}
    #assert False, repr(tabledef)
    lines = split_by(",", tabledef[1:-1])
    for line in lines:
        tokens = line
        name = tokens[0]
        typedef = tokens[1:]
        if contains(typedef, ["TIMESTAMP", "WITH", "TIME", "ZONE"]):
            desc = ["TIMESTAMP+TZ"]
        else:
            desc = [typedef[0]]
        if not contains(typedef, ["NOT", "NULL"]):
            desc.append("NULL")
        res[tokens[0]] = desc
    return res

def parse_file(fname):
    with open(fname) as f:
        content = f.read()
    return json.dumps(parse(content))

if __name__ == "__main__":
    print(parse_file(sys.argv[1]))
