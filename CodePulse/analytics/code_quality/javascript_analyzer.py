import re


def analyze_javascript(file_path):
    """
    Analyze a JavaScript source file using
    lightweight static analysis.
    """

    result = {
        "language": "JavaScript",
        "supported": True,
        "lines_of_code": 0,
        "functions": 0,
        "classes": 0,
        "imports": 0,
        "complexity": 0,
        "max_nesting": 0,
        "issues": [],
    }

    # ========================================
    # Read source file
    # ========================================

    try:

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:

            source = file.read()

    except (
        UnicodeDecodeError,
        OSError
    ):

        result["supported"] = False

        result["issues"].append(
            "Unable to read source file."
        )

        return result

    # ========================================
    # Lines of code
    # ========================================

    lines = source.splitlines()

    result["lines_of_code"] = len(lines)

    # ========================================
    # Imports
    # ========================================

    import_patterns = [
        r"\bimport\s+",
        r"\brequire\s*\("
    ]

    for pattern in import_patterns:

        result["imports"] += len(
            re.findall(
                pattern,
                source
            )
        )

    # ========================================
    # Functions
    # ========================================

    function_patterns = [
        r"\bfunction\s+\w+\s*\(",
        r"\basync\s+function\s+\w+\s*\(",
        r"\b\w+\s*=\s*(?:async\s*)?\([^)]*\)\s*=>",
        r"\([^)]*\)\s*=>",
    ]

    functions_found = set()

    for pattern in function_patterns:

        matches = re.finditer(
            pattern,
            source
        )

        for match in matches:

            functions_found.add(
                match.start()
            )

    result["functions"] = len(
        functions_found
    )

    # ========================================
    # Classes
    # ========================================

    result["classes"] = len(
        re.findall(
            r"\bclass\s+\w+",
            source
        )
    )

    # ========================================
    # Complexity
    # ========================================

    complexity_patterns = [
        r"\bif\s*\(",
        r"\belse\s+if\s*\(",
        r"\bfor\s*\(",
        r"\bwhile\s*\(",
        r"\bswitch\s*\(",
        r"\bcatch\s*\(",
        r"\?\?",
        r"\?",
        r"&&",
        r"\|\|",
    ]

    complexity = 1

    for pattern in complexity_patterns:

        complexity += len(
            re.findall(
                pattern,
                source
            )
        )

    result["complexity"] = complexity

    # ========================================
    # Maximum nesting
    # ========================================

    current_depth = 0
    maximum_depth = 0

    for character in source:

        if character == "{":

            current_depth += 1

            maximum_depth = max(
                maximum_depth,
                current_depth
            )

        elif character == "}":

            current_depth = max(
                0,
                current_depth - 1
            )

    result["max_nesting"] = (
        maximum_depth
    )

    # ========================================
    # Long functions
    # ========================================

    for match in re.finditer(
        r"(?:function\s+\w+|=>)\s*",
        source
    ):

        start_position = match.start()

        line_number = (
            source[:start_position].count("\n")
            + 1
        )

        remaining_source = source[
            start_position:
        ]

        opening_brace = (
            remaining_source.find("{")
        )

        if opening_brace == -1:
            continue

        function_body = remaining_source[
            opening_brace:
        ]

        depth = 0
        end_position = None

        for index, character in enumerate(
            function_body
        ):

            if character == "{":

                depth += 1

            elif character == "}":

                depth -= 1

                if depth == 0:

                    end_position = index

                    break

        if end_position is None:
            continue

        function_source = (
            function_body[
                :end_position + 1
            ]
        )

        function_lines = (
            function_source.count("\n")
            + 1
        )

        if function_lines > 50:

            result["issues"].append({
                "type": "Long Function",
                "name": "JavaScript Function",
                "line": line_number,
                "details": (
                    f"{function_lines} lines"
                ),
            })

    # ========================================
    # Deep nesting
    # ========================================

    if maximum_depth > 4:

        result["issues"].append({
            "type": "Deep Nesting",
            "name": "JavaScript Code",
            "line": 1,
            "details": (
                f"Nesting depth: "
                f"{maximum_depth}"
            ),
        })

    # ========================================
    # High complexity
    # ========================================

    if complexity > 10:

        result["issues"].append({
            "type": "High Complexity",
            "name": "JavaScript Code",
            "line": 1,
            "details": (
                f"Complexity: "
                f"{complexity}"
            ),
        })

    return result