# One Line Compiler

One line Compiler is a program that takes a custom programming language based on Python and turns it into one line of Python code.

### This project has absolutely no intention of being a safe and usable compiler for productions.

Your code could be buggy and the memory usage could be terrible!
Use it with caution!

## Available features

One Line Compiler has support for:
- Basic function call
- variable assigment
- lib imports
- procedures (functions that return the value of the last expression of the function)
- functions (functions that return the given data)
- class (with inheritance)
- conditions
- for loop
- main loop

## How to use?

Create a text file to write your code.

You can run the compiler with `python .\one_line_compiler.py .\one_line_in.txt` as exemple.

In OLC lang, you have access to 2 code blocks: `Init` and `Loop`. In the `Init` field, add all the code you need to run once at the begginning of your program. In the `loop` field, add all the code you need to run indefinitely like in a `while True` field. You can request the end off the loop just by adding `exit` in your code.

Here is an exemple:
```python
#Init
my_var = "Hello, World!"
print(my_var)
print("This print is called once!")

#Loop
print("I can't stop running!!")
```
