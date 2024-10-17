import ast
from textwrap import dedent
from unittest import mock

from lib.txscript.txscript.formula import Formula


def test_dependencies_and_targets() -> None:
    formula = Formula(
        "field",
        dedent(
            """
        show_info('info', field=field.info)
        show_warning('warning', field.warning)
        show_error('error', field.error)
        show_error('error')
        automation_blocker('blocker', field.blocker)
        automation_blocker('blocker')
        field.xyz
        field._index
        field.abc
        """
        ),
    )

    assert sorted(formula.dependencies) == ["abc", "xyz"]
    assert sorted(formula.targets) == ["blocker", "error", "info", "warning"]


def test_evaluate_parses_ast_just_once() -> None:
    class TxScriptX:
        def _formula_methods(self):
            return {}

    with mock.patch("ast.parse", wraps=ast.parse) as ast_parse:
        formula = Formula("field", "0")
        formula.evaluate(TxScriptX())
        formula.evaluate(TxScriptX())

    ast_parse.assert_called_once()
