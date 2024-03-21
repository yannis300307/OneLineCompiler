with open("one_line_in.txt", "r") as file:
    data_ = file.read()


def eval_block(data):
    out = []
    if isinstance(data, str):
        lines = data.split("\n")
    else:
        lines = data
    i = 0
    while i != len(lines):
        j = lines[i]
        if j == "" or j.startswith("#"):
            i += 1
            continue
        if j.startswith("exit"):
            out.append("__exit__:=True")
        elif j.startswith("import"):
            libs = j.split()[1:]
            for lib in libs:
                out.append(f"{lib}:=__import__(\"{lib}\")")
        elif j.count("=") == 1 and compile(j, "", "exec"):
            operands = j.split("=")
            out.append(operands[0] + ":=" + operands[1])
        elif j.startswith("for"):
            block_lines = []
            indent_len = 0
            for_line = j
            for k in lines[i+1]:
                if k == " ":
                    indent_len += 1
                else:
                    break
            i += 1
            indent = indent_len
            while indent >= indent_len and i < len(lines):
                indent = 0
                for k in lines[i]:
                    if k == " ":
                        indent += 1
                    else:
                        break
                if indent >= indent_len:
                    block_lines.append(lines[i][indent_len:])
                i += 1
            block = eval_block(block_lines)
            out.append("_:=[(" + ", ".join(block) + ") " + for_line + "]")
            i -= 1
        elif j.startswith("if"):
            block_lines = []
            indent_len = 0
            if_line = j
            for k in lines[i + 1]:
                if k == " ":
                    indent_len += 1
                else:
                    break
            i += 1
            indent = indent_len
            while indent >= indent_len and i < len(lines):
                indent = 0
                for k in lines[i]:
                    if k == " ":
                        indent += 1
                    else:
                        break
                if indent >= indent_len:
                    block_lines.append(lines[i][indent_len:])
                i += 1
            block = eval_block(block_lines)
            out.append("_:=((" + ", ".join(block) + ") " + if_line + " else None)")
            i -= 1
        else:
            out.append(j)
        i += 1
    return out


init_start = 0
loop_start = 0
found_init = False
found_loop = False
lines = data_.split("\n")

for i in enumerate(lines):
    if i[1].startswith("#Init"):
        init_start = i[0]
        found_init = True
    elif i[1].startswith("#Loop"):
        loop_start = i[0]
        found_loop = True
if not found_loop:
    loop_start = len(lines)-1

init_lines = eval_block(lines[init_start:loop_start+1])
loop_lines = eval_block(lines[loop_start:])

result = f"while ('__exit__' not in globals()): _=((" + (f"_:=({','.join(init_lines)}, __inited__:=True) if (not '__inited__' in globals()) else None," if found_init else "") + (f"({','.join(loop_lines)})))" if found_loop else "))")

print(result)
