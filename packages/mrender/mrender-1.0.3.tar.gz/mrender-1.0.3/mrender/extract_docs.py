from __future__ import annotations

import ast
import importlib
import inspect
import textwrap
import pyclbr
import pydoc
from typing import Any, Type, Union
from types import ModuleType
import traceback
import contextlib


class DocstringVisitor(ast.NodeVisitor):
    def __init__(self) -> None:
        super().__init__()
        self.target: str | None = None
        self.attrs: dict[str, str] = {}
        self.previous_node_type: type[ast.AST] | None = None

    def visit(self, node: ast.AST) -> Any:
        node_result = super().visit(node)
        self.previous_node_type = type(node)
        return node_result

    def visit_AnnAssign(self, node: ast.AnnAssign) -> Any:
        if isinstance(node.target, ast.Name):
            self.target = node.target.id

    def visit_Expr(self, node: ast.Expr) -> Any:
        if (
            isinstance(node.value, ast.Constant)
            and isinstance(node.value.value, str)
            and self.previous_node_type is ast.AnnAssign
        ):
            docstring = inspect.cleandoc(node.value.value)
            if self.target:
                self.attrs[self.target] = docstring
            self.target = None


def _dedent_source_lines(source: list[str]) -> str:
    if not isinstance(source, list) and not isinstance(source, str):
        return inspect.getsource(source)
    dedent_source = textwrap.dedent("".join(source))
    return dedent_source


def _extract_source_from_frame(cls: type[Any]) -> list[str] | None:
    block_lines = inspect.getsource(cls)
    dedent_source = _dedent_source_lines(block_lines)
    with contextlib.suppress(SyntaxError):
        block_tree = ast.parse(dedent_source)

        stmt = block_tree.body[0]
        if isinstance(stmt, ast.FunctionDef) and stmt.name == "dedent_workaround":
            stmt = stmt.body[0]

    return stmt.body


def extract_docstrings_from_cls(cls: type[Any], use_inspect: bool = False) -> dict[str, str]:
    """Map model attributes and their corresponding docstring."""
    if use_inspect:
        try:
            source, _ = inspect.getsourcelines(cls)
        except OSError:
            return {}
    else:
        source = _extract_source_from_frame(cls)
    dedent_source = _dedent_source_lines(source)
    visitor = DocstringVisitor()
    visitor.visit(ast.parse(dedent_source))
    return visitor.attrs


def bfs_explore_module(
    module: ModuleType, depth: int = 1, include_signatures: bool = True, include_docstrings: bool = True
) -> dict[str, dict[str, str]]:
    """Explore the module using BFS and extract signatures/docstrings up to a certain depth."""
    result = {}

    def explore_item(item, current_depth: int):
        if current_depth > depth:
            return

        item_name = item.__name__
        result[item_name] = {}

        if include_signatures and (inspect.isfunction(item) or inspect.isclass(item)):
            result[item_name]["signature"] = str(inspect.signature(item))

        if include_docstrings:
            doc = inspect.getdoc(item)
            if doc:
                doc_head, doc_body = pydoc.splitdoc(doc)
                result[item_name]["docstring_head"] = doc_head
                result[item_name]["docstring_body"] = doc_body

        if inspect.isclass(item):
            for attr_name, attr_value in inspect.getmembers(item):
                if inspect.isfunction(attr_value) or inspect.isclass(attr_value):
                    explore_item(attr_value, current_depth + 1)

    for attr_name, attr_value in inspect.getmembers(module):
        if inspect.isfunction(attr_value) or inspect.isclass(attr_value):
            explore_item(attr_value, 1)

    return result


def extract_docstring_from_object(
    obj: Union[str, ModuleType, Type, None],
    depth: int = 1,
    include_signatures: bool = True,
    include_docstrings: bool = True,
) -> dict[str, dict[str, str]]:
    """Extract docstrings and signatures from a module or class with BFS and depth control."""
    try:
        # If it's a module name as string, import it
        if isinstance(obj, str):
            obj = importlib.import_module(obj)

        # Explore module attributes if it's a module
        if isinstance(obj, ModuleType):
            return bfs_explore_module(obj, depth, include_signatures, include_docstrings)

        # If it's a class, extract class-level docstrings
        elif inspect.isclass(obj):
            return extract_docstrings_from_cls(obj)

    except (ImportError, AttributeError, Exception) as e:
        traceback.print_exc()
        raise ImportError(f"Could not import {obj}: {e}") from e


def search_synopsis(module_name: str) -> str:
    """Get the one-line summary out of a module file using pydoc.synopsis."""
    try:
        module_path = importlib.util.find_spec(module_name).origin
        return pydoc.synopsis(module_path)
    except Exception as e:
        return f"Could not find synopsis for {module_name}: {e}"


def search_apropos(keyword: str) -> list[str]:
    """Find all modules that match the keyword using pydoc.apropos."""
    return pydoc.apropos(keyword)


if __name__ == "__main__":
    # Example with Pydantic module
    print(extract_docstring_from_object("pydantic", depth=2, include_signatures=True, include_docstrings=True))

    # Example using pydoc.synopsis
    print(search_synopsis("pydantic"))

    # Example using pydoc.apropos
    print(search_apropos("doc"))
