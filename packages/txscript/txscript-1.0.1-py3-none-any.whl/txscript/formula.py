from __future__ import annotations

import ast
import importlib
from typing import TYPE_CHECKING, Any, Optional, Set

from .txscript import TxScriptAnnotationContent  # noqa: TC002

if TYPE_CHECKING:
    from types import CodeType


# get __dict__ with builtins of builtins.py in this directory
builtins = importlib.import_module(".builtins", __package__)


class FieldReferenceVisitor(ast.NodeVisitor):
    EXCLUDED_FIELD_IDS = {"", "_index"}
    TARGET_METHOD_NAMES = {"show_info", "show_warning", "show_error", "automation_blocker"}

    def __init__(self) -> None:
        super().__init__()
        self.schema_ids: Set[str] = set()
        self.target_schema_ids: Set[str] = set()

    def visit_Call(self, node: ast.Call) -> None:
        if getattr(node.func, "id", "") not in self.TARGET_METHOD_NAMES:
            return super().generic_visit(node)

        if len(node.args) > 1:
            field_attr = node.args[1]
        elif field_keyword := next((k for k in node.keywords if k.arg == "field"), None):
            field_attr = field_keyword.value
        else:
            field_attr = None

        if value := getattr(field_attr, "value", None):
            if getattr(value, "id", "") in ("field", "row") and (schema_id := getattr(field_attr, "attr", "")):
                self.target_schema_ids.add(schema_id)
                setattr(field_attr, "__cleared_attr", "")  # noqa: B010  # avoid in visit_Attribute below

        super().generic_visit(node)

    def visit_Attribute(self, node: ast.Attribute) -> None:
        # Catch also `row` as the iterator variable for line_item for-loops.
        if getattr(node.value, "id", "") in ("field", "row"):
            attr = getattr(node, "__cleared_attr", node.attr)
            if attr not in self.EXCLUDED_FIELD_IDS:
                self.schema_ids.add(node.attr)
        super().generic_visit(node)


class ExpressionGatheringTransformer(ast.NodeTransformer):
    def visit_Expr(self, node: ast.Expr) -> ast.Expr:
        call = ast.Call(func=ast.Name(id="_eg", ctx=ast.Load()), args=[node.value], keywords=[])
        expr = ast.Expr(value=call, lineno=0, col_offset=0)
        return expr


class ExpressionGatherer:
    def __init__(self) -> None:
        self.last_expression_result: Any = None

    def __call__(self, x: Any) -> None:
        self.last_expression_result = x


class Formula:
    def __init__(self, schema_id: str, string: str) -> None:
        self.schema_id = schema_id
        self.string = string
        self.code: Optional[CodeType] = None

        # Return value of formula is either `return` statement value or value of
        # the last executed expression.
        self.tree = ast.parse(self.string, self.schema_id, "exec")

        visitor = FieldReferenceVisitor()
        visitor.visit(self.tree)
        self.dependencies = visitor.schema_ids
        self.targets = visitor.target_schema_ids

    def evaluate(self, t: TxScriptAnnotationContent) -> Optional[Any]:
        _eg = ExpressionGatherer()

        globals_ = dict(
            **t.__dict__,
            **t._formula_methods(),
            **builtins.__dict__,
            _eg=_eg,
        )

        if not self.code:
            transformer = ExpressionGatheringTransformer()
            transformer.visit(self.tree)
            ast.fix_missing_locations(self.tree)

            filename = f"<formula:{self.schema_id}>"
            self.code = compile(self.tree, filename, "exec")

        exec(self.code, globals_)
        return _eg.last_expression_result
