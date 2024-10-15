"""Base models for the MMtx API."""

from typing import Optional, Type, Any, Tuple
from copy import deepcopy

from pydantic import BaseModel, create_model
from pydantic.fields import FieldInfo


class ListModel(BaseModel):
    """Base model for list responses

    Attributes:
        itemCount (int): Number of items in the list
        pageCount (int): Number of pages in the list
    """

    itemCount: int
    pageCount: int


def partial_model(model: Type[BaseModel]):
    """make all fields of a model optional

    Args:
        model (Type[BaseModel]): Model to make partial
    """

    def make_field_optional(
        field: FieldInfo, default: Any = None
    ) -> Tuple[Any, FieldInfo]:
        new = deepcopy(field)
        new.default = default
        new.annotation = Optional[field.annotation]  # type: ignore
        return new.annotation, new

    return create_model(
        f"Partial{model.__name__}",
        __base__=model,
        __module__=model.__module__,
        **{
            field_name: make_field_optional(field_info)
            for field_name, field_info in model.model_fields.items()
        },
    )
