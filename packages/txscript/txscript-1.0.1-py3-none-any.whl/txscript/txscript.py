from __future__ import annotations

import abc
from typing import Any, List, Optional

from .annotation import Annotation
from .datapoint import FieldValueBase  # noqa: TC002
from .exceptions import PayloadError
from .fields import Fields
from .flatdata import FieldsFlatData


class TxScriptBase(abc.ABC):
    pass


class TxScriptAnnotationContent(TxScriptBase):
    """
    This class encapsulates the annotation_content event Rossum TxScript execution context.

    Its attributes (including methods) are available as globals in formula code.
    """

    field: Fields
    annotation: Optional[Annotation]

    _messages: List[dict]
    _automation_blockers: List[dict]

    def __init__(self, field: Fields, annotation: Optional[Annotation] = None) -> None:
        self.field = field
        self.annotation = annotation

        self._messages = []
        self._automation_blockers = []

    @staticmethod
    def from_payload(payload: dict) -> TxScriptAnnotationContent:
        try:
            schema_content = payload["schemas"][0]["content"]
        except KeyError:
            raise PayloadError("Schema sideloading must be enabled!") from None
        field = Fields(FieldsFlatData.from_tree(schema_content, payload["annotation"]["content"]))

        annotation = (
            Annotation(payload["annotation"], payload.get("rossum_authorization_token", None))
            if "status" in payload["annotation"]
            else None
        )

        return TxScriptAnnotationContent(field, annotation)

    def _with_field(self, field: Fields) -> TxScriptAnnotationContent:
        t = TxScriptAnnotationContent(field, self.annotation)
        t._messages = self._messages
        t._automation_blockers = self._automation_blockers
        return t

    def hook_response(self) -> dict:
        return {
            "automation_blockers": self._automation_blockers,
            "messages": self._messages,
            "operations": self.field._get_operations(),
        }

    def _formula_methods(self) -> dict:
        return {
            "show_error": self.show_error,
            "show_warning": self.show_warning,
            "show_info": self.show_info,
            "automation_blocker": self.automation_blocker,
        }

    def show_error(self, content: str, field: Optional[FieldValueBase] = None, **json: Any) -> None:
        if field is not None:
            json = dict(**json, id=field.id)
        self._message(type="error", content=content, **json)

    def show_warning(self, content: str, field: Optional[FieldValueBase] = None, **json: Any) -> None:
        if field is not None:
            json = dict(**json, id=field.id)
        self._message(type="warning", content=content, **json)

    def show_info(self, content: str, field: Optional[FieldValueBase] = None, **json: Any) -> None:
        if field is not None:
            json = dict(**json, id=field.id)
        self._message(type="info", content=content, **json)

    def automation_blocker(self, content: str, field: Optional[FieldValueBase] = None, **json: Any) -> None:
        if field is not None:
            json = dict(**json, id=field.id)
        self._automation_blocker(content=content, **json)

    def _message(self, **json: Any) -> None:
        schema_id = json.pop("schema_id", None)
        if schema_id:
            json["id"] = self.field.__getattr__(schema_id).attr.id  # type: ignore[union-attr]
        self._messages.append(json)

    def _automation_blocker(self, **json: Any) -> None:
        schema_id = json.pop("schema_id", None)
        if schema_id:
            json["id"] = self.field.__getattr__(schema_id).attr.id  # type: ignore[union-attr]
        self._automation_blockers.append(json)


class TxScript:
    @staticmethod
    def from_payload(payload: dict) -> TxScriptBase:
        if payload["event"] == "annotation_content":
            return TxScriptAnnotationContent.from_payload(payload)
        else:
            raise ValueError(f"Event not supported by TxScript: {payload['event']}")
