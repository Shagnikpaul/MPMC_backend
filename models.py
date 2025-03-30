from pydantic import BaseModel, Field
from typing import Optional, List
from bson import ObjectId
from typing import Annotated, Any, Callable
from pydantic_core import core_schema
from datetime import datetime
# Custom ObjectId type for Pydantic


class _ObjectIdPydanticAnnotation:
    # Based on https://docs.pydantic.dev/latest/usage/types/custom/#handling-third-party-types.

    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        _source_type: Any,
        _handler: Callable[[Any], core_schema.CoreSchema],
    ) -> core_schema.CoreSchema:
        def validate_from_str(input_value: str) -> ObjectId:
            return ObjectId(input_value)

        return core_schema.union_schema(
            [
                core_schema.is_instance_schema(ObjectId),
                core_schema.no_info_plain_validator_function(
                    validate_from_str),
            ],
            serialization=core_schema.to_string_ser_schema(),
        )

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


PydanticObjectId = Annotated[
    ObjectId, _ObjectIdPydanticAnnotation
]


class TollModelIn(BaseModel):
    plate_number: str
    toll_fee: int
    time: datetime
    toll_location: Optional[str] = "Unknown Toll Location"


class TollModelOut(BaseModel):
    id: Optional[PydanticObjectId] = Field(alias='_id')
    plate_number: str
    toll_fee: int
    time: datetime
    toll_location: Optional[str] = "Unknown Toll Location"


class TollsModel(BaseModel):
    due_amount: Optional[float] = 0.0
    tolls: List[TollModelOut]
    
