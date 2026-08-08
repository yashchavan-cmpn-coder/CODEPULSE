from analytics.code_quality.repository_analyzer import (
    analyze_repository
)


# ========================================
# Repository to analyze
# ========================================

repository_path = (
    r"C:\Users\yashh\OneDrive\Desktop\CodePulse\CodePulse"
)


# ========================================
# Run analysis
# ========================================

result = analyze_repository(
    repository_path
)


# ========================================
# Repository Summary
# ========================================

print("\n==============================")
print("CODE QUALITY ANALYSIS")
print("==============================")

print(
    "Files analyzed:",
    result["files_analyzed"]
)

print(
    "Lines of code:",
    result["lines_of_code"]
)

print(
    "Functions:",
    result["functions"]
)

print(
    "Classes:",
    result["classes"]
)

print(
    "Imports:",
    result["imports"]
)

print(
    "Total complexity:",
    result["complexity"]
)

print(
    "Maximum nesting:",
    result["max_nesting"]
)


# ========================================
# Languages
# ========================================

print("\nLANGUAGES")
print("------------------------------")

if result["languages"]:

    for language, data in result[
        "languages"
    ].items():

        print(
            language,
            "-",
            data["files"],
            "files -",
            data["lines"],
            "lines"
        )

else:

    print("No supported languages found.")


# ========================================
# Code Quality Issues
# ========================================

print("\nCODE QUALITY ISSUES")
print("------------------------------")

if not result["issues"]:

    print("No issues found.")

else:

    for issue in result["issues"]:

        if isinstance(issue, dict):

            print(
                f'{issue["type"]} | '
                f'{issue["file"]} | '
                f'{issue["name"]} | '
                f'Line {issue["line"]} | '
                f'{issue["details"]}'
            )

        else:

            print(issue)


# ========================================
# File-Level Analysis
# ========================================

print("\nFILE ANALYSIS")
print("------------------------------")

if not result["files"]:

    print("No files analyzed.")

else:

    for file_data in result["files"]:

        print(
            "\nFile:",
            file_data["file"]
        )

        print(
            "Language:",
            file_data["language"]
        )

        print(
            "Lines:",
            file_data["lines_of_code"]
        )

        print(
            "Functions:",
            file_data["functions"]
        )

        print(
            "Classes:",
            file_data["classes"]
        )

        print(
            "Imports:",
            file_data["imports"]
        )

        print(
            "Complexity:",
            file_data["complexity"]
        )

        print(
            "Maximum nesting:",
            file_data["max_nesting"]
        )

        print(
            "Issues:",
            len(file_data["issues"])
        )