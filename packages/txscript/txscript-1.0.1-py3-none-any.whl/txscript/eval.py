from __future__ import annotations

from html import escape
from typing import TYPE_CHECKING, Any, Dict, List, Tuple

from .datapoint import Field, MultivalueDatapointField
from .formula import Formula

if TYPE_CHECKING:
    from .txscript import TxScriptAnnotationContent


def toposort(formulas: List[Formula]) -> List[Formula]:
    formula_by_schema_id = {f.schema_id: f for f in formulas}

    sorted_formulas = []

    while formulas:
        independent_formulas = [
            f for f in formulas if all(dep not in formula_by_schema_id or dep == f.schema_id for dep in f.dependencies)
        ]
        if not independent_formulas:
            raise RuntimeError(f"Cyclical dependencies: {', '.join(f.schema_id for f in formulas)}")
        for f in independent_formulas:
            del formula_by_schema_id[f.schema_id]
            sorted_formulas.append(f)
            formulas.remove(f)

    return sorted_formulas


def format_formula_exception(formula: Formula, e: Exception) -> Tuple[str, int]:
    lines = [""] + formula.string.split("\n")

    result = [str(e), "", "Traceback (most recent call last):"]
    tb = e.__traceback__
    tb_lineno = 1
    while tb:
        if tb.tb_frame.f_code.co_filename.startswith("<"):  # filter only formula source code tb_frames
            tb_lineno = tb.tb_lineno
            co_name = tb.tb_frame.f_code.co_name
            co_name = co_name if co_name != "<module>" else tb.tb_frame.f_code.co_filename
            result.append(f"  at line {tb_lineno}, in {co_name}:")
            result.append(f"    {lines[tb_lineno].strip()}")
        tb = tb.tb_next

    formatted_tb = "\n".join(result)
    return f"{e.__class__.__name__}: {formatted_tb}", tb_lineno


def create_exception_message(formula: Formula, content: str, lineno: int) -> dict:
    return {
        "schema_id": formula.schema_id,
        "type": "error",
        "content": escape(content).replace("\n", "<br>").replace("  ", "&nbsp;&nbsp;"),
        "detail": {"is_exception": True, "traceback_line_number": lineno},
    }


def eval_field(
    t: TxScriptAnnotationContent,
    _readonly_context: Any,
    formula: Formula,
    formula_field: Field,
    debug: bool = False,
) -> None:
    try:
        if formula_field.attrs.get("no_recalculation", False):
            if debug:
                print(f"{formula.schema_id}: (no recalculation)")
            return

        with _readonly_context():
            new_val = formula.evaluate(t)

        t.field.__setattr__(formula.schema_id, new_val)

        if debug:
            print(f"{formula.schema_id}: {new_val}")
    except Exception as e:
        content, lineno = format_formula_exception(formula, e)
        print(f"{formula.schema_id} [exc]: {content}")
        t._message(**create_exception_message(formula, content, lineno))


def eval_strings(formuladict: Dict[str, str], t: TxScriptAnnotationContent, debug: bool = False) -> None:
    formulas = [Formula(schema_id, formulastr) for schema_id, formulastr in formuladict.items()]

    for formula in toposort(formulas):
        formula_field = t.field._get_field(formula.schema_id)
        multivalue_tuple = formula_field.parent if isinstance(formula_field, MultivalueDatapointField) else None

        if not multivalue_tuple:
            eval_field(t, t.field._readonly_context, formula, formula_field, debug)
        else:
            for row in multivalue_tuple.get_value():  # type: ignore[attr-defined]
                with row._row_formula_context(t) as row_r:
                    eval_field(row_r, t.field._readonly_context, formula, row._get_field(formula.schema_id), debug)
        print(f"{formula.schema_id}")
