import sys

if len(sys.argv) == 2:
    file_path = sys.argv[1]
else:
    file_path = "one_line_in.txt"

with open(file_path, "r") as file:
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
    i -= 2
    return block_lines, block_head_line, i


def eval_block(data, allow_return=False, class_=None):
    out = []
    compiled_line = None
    compiled_block = []
    if isinstance(data, str):
        lines = data.split("\n")
    else:
        lines = data
    i = 0
    while i < len(lines):
        j = lines[i]
        if j == "" or j.startswith("#") or j.count(" ") == len(j):
            i += 1
            continue
        if j.startswith("exit"):
            compiled_line = "__exit__:=True"
        elif j.startswith("proc "):
            block_lines, block_head_line, i = get_block(i, lines)

            block = eval_block(block_lines)
            function_name = block_head_line[5:block_head_line.index("(")]
            args = block_head_line[block_head_line.index("(")+1:block_head_line.rindex(")")]
            if class_ is not None:
                compiled_line = f"setattr({class_}, \"{function_name}\", lambda {args}: ({', '.join(block)},)[-1])"
            else:
                compiled_line = function_name + ":=lambda " + args + ": (" + ", ".join(block) + ", None)[-1]"
        elif j.startswith("class "):
            block_lines, block_head_line, i = get_block(i, lines)

            class_name = block_head_line.split()[1]
            class_name = class_name[0:class_name.index("(")] if "(" in class_name else class_name
            block = eval_block(block_lines, class_=class_name)

            if "(" in block_head_line:
                args = block_head_line[block_head_line.index("(") + 1:block_head_line.rindex(")")]
                if len(args.split(",")) > 1:
                    raise ValueError("Only one parent is accepted for classes.")
            else:
                args = None

            compiled_line = class_name+":=type('" + class_name + "', (" + ("object" if args is None else args) + ", ), {})"

            compiled_block = block
        elif j.startswith("func "):
            block_lines, block_head_line, i = get_block(i, lines)

            block = eval_block(block_lines, True)
            block.insert(0, "__return_value__:=None")
            block.append("__return_value__")

            function_name = block_head_line[5:block_head_line.index("(")]
            args = block_head_line[block_head_line.index("(") + 1:block_head_line.rindex(")")]
            if class_ is not None:
                compiled_line = f"setattr({class_}, \"{function_name}\", lambda {args}: ({', '.join(block)})[-1],)"
            else:
                compiled_line = function_name + ":=lambda " + args + ": (" + ", ".join(block) + ",)[-1]"
        elif j.startswith("return "):
            return_expr = j[7:]
            assert allow_return, "Return is forbidden outside of a function (not procedure)!"
            compiled_line = f"(__return_value__:=({return_expr}) if __return_value__ is None else None)"

        elif j.startswith("import "):
            print("In class :", class_)
            assert class_ is None, "Imports can't be made inside a class."
            libs = j.split()[1:]
            for lib in libs:
                compiled_line = f"{lib}:=__import__(\"{lib}\")"
        elif j.count("=") == 1 and not ((j[0:j.index("=")].count("\"") % 2 == 1 and j[j.index("="):].count("\"") % 2 == 1) or (j[0:j.index("=")].count("'") % 2 == 1 and j[j.index("="):].count("'") % 2 == 1)):
            operands = j.split("=")
            if class_ is not None:
                compiled_line = f"setattr({class_}, \"{operands[0][0:operands[0].find(' ')] if operands[0].endswith(' ') else operands[0]}\", {operands[1]})"
            elif operands[0].count(".") == 1 and operands[0].index(".") != 0:
                compiled_line = f"setattr({operands[0][0:operands[0].index('.')]}, \"{operands[0][operands[0].index('.')+1:operands[0].find(' ')] if operands[0].endswith(' ') else operands[0]}\", {operands[1]})"
            else:
                compiled_line = operands[0] + ":=" + operands[1]
        elif j.startswith("for "):
            block_lines, block_head_line, i = get_block(i, lines)

            block = eval_block(block_lines)
            compiled_line = "_:=[(" + ", ".join(block) + ") " + block_head_line + "]"
        elif j.startswith("if "):
            block_lines, block_head_line, i = get_block(i, lines)

            block = eval_block(block_lines)
            compiled_line = "_:=((" + ", ".join(block) + ") " + block_head_line + " else None)"
        else:
            compiled_line = j
        i += 1
        if compiled_line is not None:
            compile("(" + compiled_line + ")", "", "exec")  # Tests the block
            out.append(compiled_line)
            print(compiled_line)
        if compiled_block:
            out.extend(compiled_block)
            compile("(" + ",".join(compiled_block) + ")", "", "exec")  # Tests the block
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


if found_loop:
    result = f"while ('__exit__' not in globals()): _=((" + (f"_:=({','.join(init_lines)}, __inited__:=True) if (not '__inited__' in globals()) else None," if found_init else "") + (f"({','.join(loop_lines)})))" if found_loop else "))")
else:
    result = f"_=({', '.join(init_lines)})"

compile(result, "", "exec")  # Final test


print("\n\n\nResult :")
print(result)