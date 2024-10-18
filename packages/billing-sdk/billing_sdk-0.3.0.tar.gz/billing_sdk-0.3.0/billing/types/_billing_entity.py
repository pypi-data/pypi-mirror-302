from datetime import datetime
from typing import Any, ClassVar

from pydantic import VERSION as PYDANTIC_VERSION
from pydantic import BaseModel
from typing_extensions import Self

IS_PYDANTIC_V2 = PYDANTIC_VERSION.startswith("2.")

if IS_PYDANTIC_V2:
    from pydantic import ConfigDict


class BillingObject(BaseModel):
    """
    Data Transfer Object for a billing API object.
    """

    if IS_PYDANTIC_V2:
        model_config: ClassVar[ConfigDict] = ConfigDict(
            frozen=True,
        )
    else:

        class Config:
            frozen = True

    @classmethod
    def parse(cls, obj: Any) -> Self:
        if IS_PYDANTIC_V2:
            return cls.model_validate(obj)
        else:
            return cls.parse_obj(obj)


class BillingEntity(BillingObject):
    id: str
    created_at: datetime


class BillingEntityWithTimestamps(BillingEntity):
    updated_at: datetime
