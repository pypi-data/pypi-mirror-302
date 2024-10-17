## Structure Inspector

`structure_inspector` is a Python package that allows you to print the structure of complex, nested Python objects. It supports dictionaries, lists, tuples, sets, and more. You can also display lengths of lists and strings, handle circular references, and limit recursion depth.

## Installation

Install the package using pip:

```bash
pip install structure_inspector
```


## Usage


```python
from structure_inspector import StructureInspector

nested_object = {
    "name": "Farhan",
    "details": {
        "age": 35,
        "children": [
            {"name": "Atta", "age": 10},
            {"name": "Dua", "age": 5}
        ]
    },
}

inspector = StructureInspector(max_depth=3, show_lengths=True)
inspector.print_structure(nested_object)
```

## Directory Structure

```
structure_inspector/
│
├── structure_inspector/
│   ├── __init__.py
│   ├── structure_inspector.py
│
├── README.md
├── LICENSE
├── setup.py
```

```

```

#### `structure_inspector.py`

The code above will be placed in `structure_inspector/structure_inspector.py`.

#### `__init__.py`

You can create an empty `__init__.py` file in the `structure_inspector` folder so it can be treated as a package.

#### `setup.py`

Here’s the content for `setup.py`, which is required for packaging your module and uploading it to PyPI:

#### Uploading to PyPI

1. Install the required tools:

```pip

pip install setuptools wheel twine
```

2. Create distribution files:

```bash
python setup.py sdist bdist_wheel
```


3. Upload to pypi
   ```
   twine upload dist/*
   ```


### Final Thoughts:

This enhanced version of the program and package adds useful features like circular reference handling, depth limiting, and support for additional types. After packaging it up and uploading it to PyPI, users will be able to install and use it with a simple `pip install structure_inspector` command.
