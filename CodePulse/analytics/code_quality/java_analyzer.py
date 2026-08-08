import re


def analyze_java(file_path):
    """
    Analyze a Java source file using
    lightweight static analysis.
    """

    result = {
        "language": "Java",
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

    result["imports"] = len(
        re.findall(
            r"^\s*import\s+",
            source,
            re.MULTILINE
        )
    )

    # ========================================
    # Classes
    # ========================================

    result["classes"] = len(
        re.findall(
            r"\b(?:public\s+|private\s+|protected\s+)?"
            r"(?:abstract\s+|final\s+)?"
            r"class\s+\w+",
            source
        )
    )

    # ========================================
    # Methods
    # ========================================

    method_pattern = (
        r"(?:public|private|protected|static|final|"
        r"synchronized|abstract|native|\s)+"
        r"[\w<>\[\], ?]+\s+"
        r"\w+\s*"
        r"\([^)]*\)\s*"
        r"(?:throws\s+[^{]+)?"
        r"\{"
    )

    result["functions"] = len(
        re.findall(
            method_pattern,
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
        r"\bcase\s+",
        r"\bcatch\s*\(",
        r"\b&&\b",
        r"\|\|",
        r"\?",
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
    # Long methods
    # ========================================

    method_matches = re.finditer(
        method_pattern,
        source
    )

    for match in method_matches:

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

        method_body = remaining_source[
            opening_brace:
        ]

        depth = 0
        end_position = None

        for index, character in enumerate(
            method_body
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

        method_source = method_body[
            :end_position + 1
        ]

        method_lines = (
            method_source.count("\n")
            + 1
        )

        if method_lines > 50:

            result["issues"].append({
                "type": "Long Method",
                "name": "Java Method",
                "line": line_number,
                "details": (
                    f"{method_lines} lines"
                ),
            })

    # ========================================
    # Deep nesting
    # ========================================

    if maximum_depth > 4:

        result["issues"].append({
            "type": "Deep Nesting",
            "name": "Java Code",
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
            "name": "Java Code",
            "line": 1,
            "details": (
                f"Complexity: "
                f"{complexity}"
            ),
        })

    return result