import astroid as _astroid
from pylint.checkers import BaseChecker as _BaseChecker
from pylint.lint import PyLinter as _PyLinter


class VariableDeclarationChecker(_BaseChecker):
    name = "variable-declaration-checker"
    msgs = {
        "W5901": ("Declare the variable with type annotation.",
                  "un-declared-variable",
                  "It's the first time the variable appears, so here should be a type annotation."),
        "W5902": ("Remove the type annotation, or rename the variable.",
                  "re-declared-variable",
                  "The variable has been used before, so here shouldn't be a type annotation."),
    }

    @staticmethod
    def _find_non_locals(body: list[_astroid.nodes.NodeNG]):
        # 这里只是简单检查一下最外面一层有没有 nonlocal ，
        # 但事实上 nonlocal 可以写在 if 等语句里面
        result: set[str] = set()
        for node in body:
            if isinstance(node, _astroid.Nonlocal):
                for name in node.names:
                    result.add(name)
        return result

    def _check(self,
               locals_dictionary: dict[str, list[_astroid.nodes.NodeNG]],
               body: list[_astroid.nodes.NodeNG]):
        # astroid 会在 locals 中包含 nonlocal 的变量，详见：
        # https://github.com/pylint-dev/astroid/issues/2616
        non_locals = VariableDeclarationChecker._find_non_locals(body)
        for name, occurrences in locals_dictionary.items():
            if name == "_":
                continue
            if name in non_locals:
                continue

            occurrence_iterator = iter(occurrences)
            occurrence = next(occurrence_iterator)

            if (
                    isinstance(occurrence, _astroid.nodes.AssignName) and
                    (not isinstance(occurrence.parent, _astroid.nodes.AnnAssign)) and
                    (not isinstance(occurrence.parent, _astroid.nodes.Arguments)) and
                    (not isinstance(occurrence.parent, _astroid.nodes.TypeAlias))
            ):
                self.add_message("un-declared-variable", node=occurrence)

            for occurrence in occurrence_iterator:
                if (
                        isinstance(occurrence.parent, _astroid.nodes.AnnAssign)
                ):
                    self.add_message("re-declared-variable", node=occurrence)

    def visit_functiondef(self, node: _astroid.nodes.FunctionDef):
        self._check(node.locals, node.body)

    def visit_module(self, node: _astroid.nodes.Module):
        self._check(node.locals, node.body)

    def visit_classdef(self, node: _astroid.nodes.ClassDef):
        self._check(node.locals, node.body)

def register(linter: _PyLinter) -> None:
    linter.register_checker(VariableDeclarationChecker(linter))
