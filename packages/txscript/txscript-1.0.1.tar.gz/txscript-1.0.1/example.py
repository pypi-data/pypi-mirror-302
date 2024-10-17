#!/usr/bin/env python3
"""
Standalone executable script that evaluates example code within the runtime.
"""


# flake8: noqa

import json

from txscript.eval import eval_custom_function, eval_strings
from txscript.fields import Fields
from txscript.flatdata import FieldsFlatData
from txscript.formula import Formula
from txscript.txscript import TxScriptAnnotationContent

if __name__ == "__main__":
    with open("examples/standalone/annotation.json", "r") as f:
        annotation = json.load(f)
    with open("examples/standalone/schema.json", "r") as f:
        schema = json.load(f)
    field = Fields(FieldsFlatData.from_tree(schema["content"], annotation["content"]))
    t = TxScriptAnnotationContent(field)

    formulas = {
        "amount_total": "field.amount_total_base + field.amount_total_tax",
        "amount_total_base": """
x = 0
for row in field.line_items:
    x += default_to(row.item_amount_base, 0)
x
        """,
        "amount_total_tax": """
sum(default_to(field.item_amount.all_values, field.item_amount_total.all_values) - field.item_amount_base.all_values)
        """,
        "terms": """
date_delta = field.date_due - field.date_issue
date_delta.days + 1
        """,
        "date_due": """
if field.date_due < field.date_issue:
    field.date_issue + timedelta(days=30)
else:
    field.date_due
        """,
        "date_issue": "date.today()",
        "item_description": "field.item_description.replace('\\n', ' ') + field.sender_name",
        "sender_name": """  # serverless function; in field fo
if field.sender_name != "":
    show_error("not empty")""",
        "sender_vat_id": """
substitute(r"[^\\w\\d]", r"", field.sender_vat_id)
        """,
        "notes": """
if field.notes.startswith("abc"):
   show_info("abv", field.notes)
if field.date_uzp == None:
   show_info("yay", field.date_uzp)
        """,
    }
    eval_strings(formulas, t, debug=True)

    Formula("", 'if not is_empty(field.order_id): show_error("tricky stuff", field.order_id)').evaluate(t)
    Formula("", 'automation_blocker(content="global automation blocker")').evaluate(t)

    print(json.dumps(t.field._get_operations()))
    print(t.field._get_operations())
    print(t._messages)
    print(t._automation_blockers)
