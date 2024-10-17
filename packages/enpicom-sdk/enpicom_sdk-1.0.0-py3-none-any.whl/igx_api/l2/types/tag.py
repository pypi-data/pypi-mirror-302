from enum import Enum
from typing import NewType

from typing_extensions import assert_never

from igx_api.l1 import openapi_client
from igx_api.l2.util.from_raw_model import FromRawModel

TagId = NewType("TagId", int)
"""The unique identifier of a tag"""

TagKey = str
"""The display name of a tag"""

TagValue = bool | int | float | str
"""The value name of a tag"""


class TagLevel(str, Enum):
    COLLECTION = "collection"
    CLONE = "clone"
    SEQUENCE = "sequence"
    FILE = "file"
    CLONE_CONTEXTUAL = "clone_contextual"


class TagDataType(str, Enum):
    AMINO_ACID_SEQUENCE = "amino_acid_sequence"
    NUCLEOTIDE_SEQUENCE = "nucleotide_sequence"
    QUALITY_SEQUENCE = "quality_sequence"
    BOOLEAN = "boolean"
    DECIMAL = "decimal"
    INTEGER = "integer"
    TEXT = "text"


class TagAccessType(str, Enum):
    MUTABLE = "mutable"
    MUTABLE_NON_DELETABLE = "mutable_non_deletable"
    IMMUTABLE = "immutable"


class TagArchetype(FromRawModel[openapi_client.GetTagsSuccessResponseTagArchetypesInner]):
    id: TagId
    key: TagKey
    level: TagLevel
    data_type: TagDataType
    access_type: TagAccessType

    @classmethod
    def _build(cls, raw: openapi_client.GetTagsSuccessResponseTagArchetypesInner) -> "TagArchetype":
        return cls(
            id=TagId(int(raw.id)), key=raw.key, level=TagLevel(raw.level), data_type=TagDataType(raw.data_type), access_type=TagAccessType(raw.access_type)
        )


class Tag(FromRawModel[openapi_client.models.TagsInner]):
    id: TagId
    value: TagValue

    @classmethod
    def _build(cls, raw: openapi_client.models.TagsInner) -> "Tag":
        def get_tag_value(x: openapi_client.models.TagValue) -> TagValue:
            # It will never be None, then something weird failed with Pydantic
            if x.actual_instance is None:
                raise ValueError("Tag value is None")
            else:
                if isinstance(x.actual_instance, bool):
                    return x.actual_instance
                elif isinstance(x.actual_instance, int):
                    return x.actual_instance
                elif isinstance(x.actual_instance, float):
                    return x.actual_instance
                elif isinstance(x.actual_instance, str):
                    return x.actual_instance
                else:
                    assert_never(x.actual_instance)

        tag_value = get_tag_value(raw.value)

        return cls(id=TagId(int(raw.id)), value=tag_value)
