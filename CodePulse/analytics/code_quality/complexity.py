import ast


class ComplexityAnalyzer(ast.NodeVisitor):

    def __init__(self):
        self.complexity = 1
        self.max_nesting = 0
        self.current_nesting = 0

    def _enter_nesting(self, node):
        self.current_nesting += 1

        self.max_nesting = max(
            self.max_nesting,
            self.current_nesting
        )

        self.generic_visit(node)

        self.current_nesting -= 1

    def visit_If(self, node):
        self.complexity += 1
        self._enter_nesting(node)

    def visit_For(self, node):
        self.complexity += 1
        self._enter_nesting(node)

    def visit_AsyncFor(self, node):
        self.complexity += 1
        self._enter_nesting(node)

    def visit_While(self, node):
        self.complexity += 1
        self._enter_nesting(node)

    def visit_ExceptHandler(self, node):
        self.complexity += 1
        self.generic_visit(node)

    def visit_BoolOp(self, node):
        self.complexity += len(node.values) - 1
        self.generic_visit(node)

    def visit_With(self, node):
        self._enter_nesting(node)

    def visit_AsyncWith(self, node):
        self._enter_nesting(node)


def calculate_complexity(node):

    analyzer = ComplexityAnalyzer()

    analyzer.visit(node)

    return {
        "complexity": analyzer.complexity,
        "max_nesting": analyzer.max_nesting,
    }