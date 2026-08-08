from .python_analyzer import analyze_python
from .javascript_analyzer import analyze_javascript
from .java_analyzer import analyze_java
from .cpp_analyzer import analyze_cpp


def analyze_file(file_path, language):
    """
    Select the appropriate analyzer based on programming language.
    """

    language = language.lower()

    if language == "python":
        return analyze_python(file_path)

    elif language in [
        "javascript",
        "js",
        "typescript",
        "ts"
    ]:
        return analyze_javascript(file_path)

    elif language in [
        "java"
    ]:
        return analyze_java(file_path)

    elif language in [
        "c++",
        "cpp"
    ]:
        return analyze_cpp(file_path)

    return {
        "language": language,
        "supported": False,
        "lines_of_code": 0,
        "functions": 0,
        "classes": 0,
        "imports": 0,
        "complexity": 0,
        "max_nesting": 0,
        "issues": [],
    }