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

You can use `if` and `for` statements like this:
```python
# Init
for i in range(5)
    print("index :", i)
    for j in range(3)
               print("You are free to use the indents you want!")

#Loop

if input("Do you want to stop ? ") == "yes"
    print("Goodbye!")
    exit
```
Note that for technical reasons, the for loop will store all the results of the functions in the for statement until the loop is finished. So pay attention to the memory usage!

You can create variables as in Python:
```python
#Init
my_var = "Hello, World!"
print(my_var)

exit
```

You can use python libs like this:
```python
#Init
import time os pygame
import lib
import myLib

print("Please wait a few seconds...")
time.sleep(2)
print("done !")

exit
```

For optimisations, there is 2 types of "functions" : The `procedures` and the `functions`. The `procedure` returns the result of the last expression. The `functions` returns the result of the expression after the `return` keyword. The only difference with the build-in python functions are that the function will not stop after a `return`. It will register the result in memory and will return it at the end of the function's execution.

Here is an exemple:
```python
#Init

proc myProcedure(a, b)
    print(f"{a}" + {b} = {a + b}")

func myFunction(a, b)
    return a + b
    print("This function is called too.")

a = 0
b = 0

#Loop

result = myFunction(a, b)

print("Result :", result)
myProcedure(a, b)

if a >= 10
    exit
```

You can use classes as in python:

```python
#Init
class myClass
    test = "yes"
    
    func test2(self, a, b)
        print(self.test)
        self.test = "no"
        return a*b

class otherClass(myClass)
    yes = "maybe"

my_object = otherClass()

for _ in range(4)
    result = my_object.test2(5, 6)
    print(result)

exit
```

Note that the `__exited__` and `__inited__` global variables are reserved.

## Why would I need to write my code in only one line?

There are no reasons other than debugging and code obfuscation. You can, however use it to troll your friends (and this is the best reason ! 😉).
