class StructureInspector:
    """
    Class to inspect and print the structure of complex Python objects.
    """

    def __init__(self, max_depth: int = None, show_lengths: bool = True):
        """
        Initialize the StructureInspector.

        :param max_depth: Maximum recursion depth for nested objects (None for no limit).
        :param show_lengths: Whether to show lengths for strings, lists, etc.
        """
        self.max_depth = max_depth
        self.show_lengths = show_lengths
        self.visited_objects = set()  # Track visited objects for circular reference detection

    def print_structure(self, obj, indent: int = 0, depth: int = 0):
        """
        Recursively print the structure of a Python object.

        :param obj: The object to inspect.
        :param indent: Current indentation level.
        :param depth: Current recursion depth.
        """
        if self.max_depth is not None and depth > self.max_depth:
            print(' ' * indent + "...")
            return

        obj_id = id(obj)
        if obj_id in self.visited_objects:
            print(' ' * indent + f"<Circular reference to object id {obj_id}>")
            return

        # Mark this object as visited
        self.visited_objects.add(obj_id)

        obj_type = type(obj).__name__
        base_indent = ' ' * indent

        # Handle different types of objects
        if isinstance(obj, str):
            length_info = f" (len: {len(obj)})" if self.show_lengths else ""
            print(f"{base_indent}String: '{obj}'{length_info}")
        elif isinstance(obj, list):
            length_info = f" (len: {len(obj)})" if self.show_lengths else ""
            print(f"{base_indent}List:{length_info}")
            for index, item in enumerate(obj):
                print(f"{base_indent}    Index {index} ->", end=" ")
                self.print_structure(item, indent + 8, depth + 1)
        elif isinstance(obj, tuple):
            length_info = f" (len: {len(obj)})" if self.show_lengths else ""
            print(f"{base_indent}Tuple:{length_info}")
            for index, item in enumerate(obj):
                print(f"{base_indent}    Index {index} ->", end=" ")
                self.print_structure(item, indent + 8, depth + 1)
        elif isinstance(obj, set):
            length_info = f" (len: {len(obj)})" if self.show_lengths else ""
            print(f"{base_indent}Set:{length_info}")
            for item in obj:
                self.print_structure(item, indent + 4, depth + 1)
        elif isinstance(obj, dict):
            length_info = f" (len: {len(obj)})" if self.show_lengths else ""
            print(f"{base_indent}Dict:{length_info}")
            for key, value in obj.items():
                print(f"{base_indent}    Key: {key} ->", end=" ")
                self.print_structure(value, indent + 8, depth + 1)
        elif isinstance(obj, (int, float, bool, type(None))):
            # Print simple types
            print(f"{base_indent}Value: {repr(obj)} ({obj_type})")
        else:
            print(f"{base_indent}Unknown type: {obj_type}")

        # Remove the object from visited set after processing
        self.visited_objects.remove(obj_id)

# Example Usage
if __name__ == "__main__":
    nested_object = {
        "name": "Farhan",
        "details": {
            "age": 35,
            "children": [
                {"name": "Atta", "age": 10},
                {"name": "Dua", "age": 5}
            ],
            "location": ("city", "country")
        },
        "hobbies": ["coding", "reading", {"outdoor": ["cricket", "running"]}],
        "active": True
    }

    inspector = StructureInspector(max_depth=3, show_lengths=True)
    inspector.print_structure(nested_object)
