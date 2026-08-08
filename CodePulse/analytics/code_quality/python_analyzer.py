import ast

from .complexity import calculate_complexity


def analyze_python(file_path):
    """
    Analyze a Python source file using AST.
    """

    result = {
        "language": "Python",
        "supported": True,

        # Basic metrics
        "lines_of_code": 0,
        "functions": 0,
        "classes": 0,
        "imports": 0,

        # Documentation
        "documented_functions": 0,
        "documented_classes": 0,

        # Complexity
        "complexity": 0,
        "max_nesting": 0,

        # Issues
        "issues": [],
    }

    # --------------------------------
    # Read source file
    # --------------------------------

    try:
        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:

            source = file.read()

    except (UnicodeDecodeError, OSError):

        result["supported"] = False

        result["issues"].append(
            "Unable to read source file."
        )

        return result

    # --------------------------------
    # Lines of Code
    # --------------------------------

    result["lines_of_code"] = len(
        source.splitlines()
    )

    # --------------------------------
    # Parse AST
    # --------------------------------

    try:
        tree = ast.parse(source)

    except SyntaxError as error:

        result["supported"] = False

        result["issues"].append(
            f"Syntax error at line {error.lineno}."
        )

        return result

    # --------------------------------
    # Analyze AST
    # --------------------------------

    for node in ast.walk(tree):

        # =================================
        # Functions
        # =================================

        if isinstance(
            node,
            (ast.FunctionDef, ast.AsyncFunctionDef)
        ):

            result["functions"] += 1

            # --------------------------------
            # Documentation
            # --------------------------------

            if ast.get_docstring(node):
                result["documented_functions"] += 1

            # --------------------------------
            # Function Length
            # --------------------------------

            if hasattr(node, "end_lineno"):

                function_lines = (
                    node.end_lineno
                    - node.lineno
                    + 1
                )

                if function_lines > 50:

                    result["issues"].append({
                        "type": "Long Function",
                        "name": node.name,
                        "line": node.lineno,
                        "details": (
                            f"{function_lines} lines"
                        ),
                    })

            # --------------------------------
            # Function Parameters
            # --------------------------------

            argument_count = len(
                node.args.args
            )

            if argument_count > 5:

                result["issues"].append({
                    "type": "Too Many Parameters",
                    "name": node.name,
                    "line": node.lineno,
                    "details": (
                        f"{argument_count} parameters"
                    ),
                })

            # --------------------------------
            # Complexity
            # --------------------------------

            complexity_data = calculate_complexity(node)

            function_complexity = (
                complexity_data["complexity"]
            )

            function_nesting = (
                complexity_data["max_nesting"]
            )

            # Add complexity to repository total
            result["complexity"] += function_complexity

            # Track highest nesting level
            result["max_nesting"] = max(
                result["max_nesting"],
                function_nesting
            )

            # --------------------------------
            # High Complexity
            # --------------------------------

            if function_complexity >= 8:

                result["issues"].append({
                    "type": "High Complexity",
                    "name": node.name,
                    "line": node.lineno,
                    "details": (
                        f"Complexity: "
                        f"{function_complexity}"
                    ),
                })

            # --------------------------------
            # Deep Nesting
            # --------------------------------

            if function_nesting >= 4:

                result["issues"].append({
                    "type": "Deep Nesting",
                    "name": node.name,
                    "line": node.lineno,
                    "details": (
                        f"Nesting depth: "
                        f"{function_nesting}"
                    ),
                })

        # =================================
        # Classes
        # =================================

        elif isinstance(node, ast.ClassDef):

            result["classes"] += 1

            # --------------------------------
            # Documentation
            # --------------------------------

            if ast.get_docstring(node):
                result["documented_classes"] += 1

            # --------------------------------
            # Large Class
            # --------------------------------

            if hasattr(node, "end_lineno"):

                class_lines = (
                    node.end_lineno
                    - node.lineno
                    + 1
                )

                if class_lines > 300:

                    result["issues"].append({
                        "type": "Large Class",
                        "name": node.name,
                        "line": node.lineno,
                        "details": (
                            f"{class_lines} lines"
                        ),
                    })

        # =================================
        # Imports
        # =================================

        elif isinstance(
            node,
            (ast.Import, ast.ImportFrom)
        ):

            result["imports"] += 1

    return result