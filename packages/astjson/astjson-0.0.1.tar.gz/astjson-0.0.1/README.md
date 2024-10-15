# AST to JSON Converter

This Python module provides a utility function `ast_to_json` which takes a Python Abstract Syntax Tree (AST) and converts it to a dictionary. The dictionary can be serialized to JSON. This is useful for scenarios where you need to analyze or manipulate the Python Abstract Syntax tree in a 
programming language other than Python. I tried to make the implementation similar to `ast.dump` to preserve the structure of the abstract syntax trees.


## Installation

To install this module, simply clone the repository and import the function into your Python script:

```python
import ast
from typing import Any, Dict
import json
import astjson

with open("your_python_program.py") as f:
    program = f.read()
t = ast.parse(program)
print(json.dumps(astjson.ast_to_json(t), indent=2))
```
