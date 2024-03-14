with open("one_line_in.txt", "r") as file:
    data = file.read()

init_lines = []
loop_lines = []
imports = []

lines = data.split("\n")

line_count = 1
lines_cat = 0
for i in lines:
    if i == "":
        continue
    if i.startswith("#Init"):
        lines_cat = 1
    elif i.startswith("#Loop"):
        lines_cat = 2
    else:
        if lines_cat == 1:
            if i.startswith("import"):
                imports.extend(i.split()[1:])
            else:
                if i.count("=") == 1 and compile(i, "", "exec"):
                    elems = i.split("=")
                    init_lines.append(elems[0] + ":=" + elems[1])
                else:
                    init_lines.append(i)
        elif lines_cat == 2:
            if i.count("=") == 1 and compile(i, "", "exec"):
                elems = i.split("=")
                loop_lines.append(elems[0] + ":=" + elems[1])
            else:
                loop_lines.append(i)
        else:
            raise SyntaxError(f"Erreur de syntaxe à la ligne : {line_count}.")
    line_count += 1

init_lines = [f"{j}:=__import__(\"{j}\")" for j in imports] + init_lines

print(init_lines)
result = f"while ('__exit__' not in globals()): _=(({','.join(init_lines)}, __inited__:=True) if (not '__inited__' in globals()) else None, ({','.join(loop_lines)}))"

print(result)
