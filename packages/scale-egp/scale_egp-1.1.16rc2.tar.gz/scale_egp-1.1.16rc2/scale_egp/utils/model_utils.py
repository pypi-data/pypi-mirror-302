"""
Create partial model definitions, sort of like Partial<> in TypeScript

Sources:
https://github.com/pydantic/pydantic/issues/3120#issuecomment-1528030416
https://stackoverflow.com/a/76560886
"""

from copy import deepcopy
from typing import Any, Dict, Optional, Type, TypeVar

import pydantic

PYDANTIC_V2 = hasattr(pydantic, "VERSION") and pydantic.VERSION.startswith("2.")

if PYDANTIC_V2:
    from pydantic.v1 import BaseModel as PydanticBaseModel
    from pydantic.v1 import Extra, Field, create_model
    from pydantic.v1.fields import ModelField
else:
    from pydantic import BaseModel as PydanticBaseModel
    from pydantic import Extra, Field, create_model
    from pydantic.fields import ModelField


# pylint: disable=missing-function-docstring


T = TypeVar("T", bound="BaseModel")


def dict_without_none_values(d: Dict[str, Any]) -> Dict[str, Any]:
    return {k: v for (k, v) in d.items() if v is not None}


class BaseModel(PydanticBaseModel):
    @classmethod
    def partial(cls, **kwargs):
        partial_model = make_partial_model(cls)
        return partial_model(**{k: v for (k, v) in kwargs.items() if v is not None})

    @classmethod
    def from_model(cls: Type[T], model: Optional[T] = None) -> Optional[T]:
        if not model:
            return None
        return cls.from_orm(model)

    @classmethod
    def from_dict(cls: Type[T], obj: Optional[Dict[str, Any]] = None) -> Optional[T]:
        if not obj:
            return None
        return cls.parse_obj(obj)

    @classmethod
    def from_json(cls: Type[T], json: Optional[str] = None) -> Optional[T]:
        if not json:
            return None
        return cls.parse_raw(json)

    @classmethod
    def model_fields(cls) -> Dict[str, Any]:
        return cls.__fields__

    def model_dump(self, exclude_none: bool = False) -> Dict[str, Any]:
        return self.dict(exclude_none=exclude_none)

    def model_dump_json(self, exclude_none: bool = False, exclude_unset: bool = False) -> str:
        return self.json(exclude_none=exclude_none, exclude_unset=exclude_unset)

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        allow_mutation = True
        arbitrary_types_allowed = True


class RootModel(BaseModel):
    def __getattr__(self, name):
        return self.__root__.__getattribute__(name)

    def __setattr__(self, name, value):
        return self.__root__.__setattr__(name, value)


def make_field_optional(field: ModelField, default: Any = None) -> ModelField:
    new = deepcopy(field)
    new.default = default
    new.required = False
    new.annotation = Optional[field.annotation]  # type: ignore
    return new


BaseModelT = TypeVar("BaseModelT", bound=BaseModel)


class OverridePartialModelMethods(BaseModel):
    """
    Base class of partial models
    """

    def dict(self, *args, **kwargs):
        """
        same as BaseModel.dict(), but only for fields present in the model.
        """
        return dict(super().dict(*args, exclude_unset=True, **kwargs).items())

    def json(self, *args, **kwargs):
        """
        same as BaseModel.json(), but only for fields present in the model.
        """
        return super().json(*args, exclude_unset=True, exclude_none=True, **kwargs)

    class Config:
        extra = Extra.forbid


def make_partial_model(model: Type[BaseModelT]) -> Type[BaseModelT]:
    __fields__ = {
        field_name: make_field_optional(field_info)
        for field_name, field_info in model.__fields__.items()
    }
    m: Type[BaseModelT] = create_model(
        f"Partial{model.__name__}",
        __base__=(model, OverridePartialModelMethods),  # type: ignore
        __module__=model.__module__,
    )
    m.__fields__ = __fields__
    return m


class Entity(BaseModel):
    """
    Base class for all entities
    """


class RootEntity(RootModel):
    """
    Root class for union type entities
    """


class hiddenstr(str):
    pass
