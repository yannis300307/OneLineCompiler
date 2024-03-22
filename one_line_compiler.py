with open("one_line_in.txt", "r") as file:
    data_ = file.read()


def get_block(i, lines):
    block_lines = []
    indent_len = 0
    block_head_line = lines[i]
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
    return block_lines, block_head_line, i


def eval_block(data, allow_return=False):
    out = []
    if isinstance(data, str):
        lines = data.split("\n")
    else:
        lines = data
    i = 0
    while i != len(lines):
        j = lines[i]
        if j == "" or j.startswith("#") or j.count(" ") == len(j):
            i += 1
            continue
        if j.startswith("exit"):
            out.append("__exit__:=True")
        elif j.startswith("proc"):
            block_lines, block_head_line, i = get_block(i, lines)

            block = eval_block(block_lines)
            function_name = block_head_line[4:block_head_line.index("(")]
            args = block_head_line[block_head_line.index("(")+1:block_head_line.index(")")]
            out.append(function_name + ":=lambda " + args + ": (" + ", ".join(block) + ")[-1]")
            i -= 1
        elif j.startswith("func"):
            block_lines, block_head_line, i = get_block(i, lines)

            block = eval_block(block_lines, True)
            block.insert(0, "__return_value__:=None")
            block.append("__return_value__")

            function_name = block_head_line[4:block_head_line.index("(")]
            args = block_head_line[block_head_line.index("(") + 1:block_head_line.index(")")]
            out.append(function_name + ":=lambda " + args + ": (" + ", ".join(block) + ")[-1]")
            i -= 1
        elif j.startswith("return"):
            return_expr = j[7:]
            assert allow_return, "Return is forbidden outside of a function (not procedure)!"
            out.append(f"(__return_value__:=({return_expr}) if __return_value__ is None else None)")

        elif j.startswith("import"):
            libs = j.split()[1:]
            for lib in libs:
                out.append(f"{lib}:=__import__(\"{lib}\")")
        elif j.count("=") == 1 and not ((j[0:j.index("=")].count("\"") % 2 == 1 and j[j.index("="):].count("\"") % 2 == 1) or (j[0:j.index("=")].count("'") % 2 == 1 and j[j.index("="):].count("'") % 2 == 1)):
            operands = j.split("=")
            out.append(operands[0] + ":=" + operands[1])
        elif j.startswith("for"):
            block_lines, block_head_line, i = get_block(i, lines)

            block = eval_block(block_lines)
            out.append("_:=[(" + ", ".join(block) + ") " + block_head_line + "]")
            i -= 1
        elif j.startswith("if"):
            block_lines, block_head_line, i = get_block(i, lines)

            block = eval_block(block_lines)
            out.append("_:=((" + ", ".join(block) + ") " + block_head_line + " else None)")
            i -= 1
        else:
            out.append(j)
        i += 1
    return out


init_start = 0
loop_start = 0
found_init = False
found_loop = False
program_lines = data_.split("\n")

for i_ in enumerate(program_lines):
    if i_[1].startswith("#Init"):
        init_start = i_[0]
        found_init = True
    elif i_[1].startswith("#Loop"):
        loop_start = i_[0]
        found_loop = True
if not found_loop:
    loop_start = len(program_lines)-1

init_lines = eval_block(program_lines[init_start:loop_start+1])
loop_lines = eval_block(program_lines[loop_start:])

result = f"while ('__exit__' not in globals()): _=((" + (f"_:=({','.join(init_lines)}, __inited__:=True) if (not '__inited__' in globals()) else None," if found_init else "") + (f"({','.join(loop_lines)})))" if found_loop else "))")

print(result)
