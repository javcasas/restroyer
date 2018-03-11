def parse(text):
    res = {}
    for line in text.split(";"):
        line = line.strip()
        tokens = line.split(" ")
        if not tokens:
            continue
        elif tokens[0].upper() == "CREATE" and tokens[1].upper() == "SCHEMA":
            res[tokens[2]] = {}
        elif tokens[0].upper() == "CREATE" and tokens[1].upper() == "TABLE":
            schema, table = tokens[2].split(".")
            res[schema][table] = parse_table(" ".join(tokens[3:]))
    return res

def parse_table(tabledef_):
    tabledef = tabledef_.strip()
    res = {}
    if tabledef[0] == "(" and tabledef[-1] == ")":
        tabledef = tabledef[1:-1]
        lines = tabledef.split(",")
        for line in lines:
            tokens = line.split()
            desc = [tokens[1].upper()]
            for i in range(1, len(tokens)):
                if tokens[i:i+2] == "not null".split():
                    break
            else:
                desc.append("NULL")
            res[tokens[0]] = desc
        return res
    else:
        raise Exception("Invalid table syntax")
