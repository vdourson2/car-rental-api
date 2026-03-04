from ruff.checkers import Checker
from ruff.rules import Rule


class NoPrintRule(Rule):
    code = "MY001"
    description = "Avoid using print()"

    def check(self, node, checker: Checker):
        if node.__class__.__name__ == "Call":
            if getattr(node.func, "id", None) == "print":
                checker.error(self, node)
