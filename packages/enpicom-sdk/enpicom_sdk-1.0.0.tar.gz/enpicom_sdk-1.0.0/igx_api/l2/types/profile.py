from enum import Enum
from typing import Literal, NewType, Optional, cast

from pydantic import BaseModel

from igx_api.l1 import openapi_client
from igx_api.l2.types.file import FileId
from igx_api.l2.types.tag import TagId
from igx_api.l2.util.from_raw_model import FromRawModel

QualityControlTemplateId = NewType("QualityControlTemplateId", str)
"""The unique identifier of a quality control template"""


SequenceTemplateId = NewType("SequenceTemplateId", str)
"""The unique identifier of a sequence template"""


class FileIdSelector(FromRawModel[openapi_client.SequenceTemplateSelector]):
    """A selector to match a file by its ID.

    Args:
        value (FileId): The ID of the file to match.

    Example:
        To match a file by its ID, use the `FileIdSelector` class:

        ```python
        selector = FileIdSelector(
            value=FileId("570f0f8c-33c4-4d4d-905b-87f3637d49eb")
        )
        ```
    """

    type: Literal["file_id"] = "file_id"
    value: FileId
    """The ID of the file to match."""

    @classmethod
    def _build(cls, raw: openapi_client.SequenceTemplateSelector) -> "FileIdSelector":
        return cls(type="file_id", value=FileId(cast(openapi_client.MatchAFileByItsID, raw).value))


class SequenceTemplateConfig(FromRawModel[openapi_client.ProfileWorkSequenceTemplatesInner]):
    """A configuration object specifying which files get assigned which sequence template.

    Args:
        selector (FileIdSelector): The selector to match the file.
        id (SequenceTemplateId): The ID of the sequence template to assign.

    Example:
        Assume we have a sequence template with ID 1, and we have a file with ID "a".

        If we want to assign file "a" to use the sequence template with ID 1, the configuration would look like this:

        ```python
        config = SequenceTemplateConfig(
            # We select the file
            selector=FileIdSelector(value=FileId("570f0f8c-33c4-4d4d-905b-87f3637d49eb")),
            # And specify the sequence template to use
            id=SequenceTemplateId(1)
        )
        ```
    """

    selector: FileIdSelector
    """The selector to match the file."""
    id: SequenceTemplateId
    """The ID of the sequence template to assign."""
    version: Optional[int] = None
    """The version of the sequence template to assign. If none, will default to the latest version"""

    @classmethod
    def _build(cls, raw: openapi_client.ProfileWorkSequenceTemplatesInner) -> "SequenceTemplateConfig":
        return cls(
            selector=FileIdSelector.from_raw(raw.selector),
            id=SequenceTemplateId(raw.template_id),
            version=int(raw.template_version) if raw.template_version is not None else None,
        )


class SequenceTemplate(FromRawModel[openapi_client.SequenceTemplate]):
    """A sequence template describing the structure of a raw sequencing data read."""

    id: SequenceTemplateId
    version: int
    name: str
    shared: bool
    """Whether the sequence template is shared within the organization."""
    author: str
    created_at: str
    updated_at: str

    @classmethod
    def _build(cls, raw: openapi_client.SequenceTemplate) -> "SequenceTemplate":
        return cls(
            id=SequenceTemplateId(raw.id),
            version=int(raw.version),
            name=str(raw.name),
            shared=bool(raw.shared),
            author=str(raw.author),
            created_at=str(raw.created_at),
            updated_at=str(raw.updated_at),
        )


class QualityControlTemplate(FromRawModel[openapi_client.QualityControlTemplate]):
    """A quality control template specifying the strictness of IGX-Profile."""

    id: QualityControlTemplateId
    version: int
    name: str
    shared: bool
    """Whether the quality control template is shared within the organization."""
    author: str
    created_at: str
    updated_at: str

    @classmethod
    def _build(cls, raw: openapi_client.QualityControlTemplate) -> "QualityControlTemplate":
        return cls(
            id=QualityControlTemplateId(raw.id),
            version=int(raw.version),
            name=str(raw.name),
            shared=bool(raw.shared),
            author=str(raw.author),
            created_at=str(raw.created_at),
            updated_at=str(raw.updated_at),
        )


class CloneIdExtractionSource(str, Enum):
    FILENAME = "filename"
    """Extract the clone ID from the filename."""
    HEADER = "header"
    """Extract the clone ID from the sequence headers."""


class CloneIdExtraction(BaseModel):
    """The configuration for extracting clone IDs from the input files.

    This only needs to be used when a sequence template has the option "Manually Specify Clone Identifier" enabled.

    Example:

        Assuming we have a filename structure that looks like this: `foo_clone_a_bar.fasta`, `bar_clone_b_foo.fasta`, and
        you want to extract the clone ID `a` and `b` respectively, you can use the following `CloneIdExtraction` configuration:

        ```python
        CloneIdExtraction(
            source=CloneIdExtractionSource.FILENAME,
            delimiter="_",
            index=2,
            target_tag_id=TagId(1337)  # Use the tag ID you want to store the clone ID in
        )
        ```
    """

    source: CloneIdExtractionSource
    """The source to extract the clone ID from."""
    delimiter: str | list[str]
    """The delimiter to split the source on.

    You can also specify multiple delimiters.

    Example:

        Assuming you have a header structure that looks like this: `>43370843|CloneId=Clone1|Heavy 1|Bmax=1.2`, and you
        want to extract the clone ID `Clone1` you can use the following `CloneIdExtraction` configuration:

        ```python
        CloneIdExtraction(
            source=CloneIdExtractionSource.HEADER,
            delimiter=["CloneId=", "|"],
            # Since we have multiple delimiters, the first `43270843` is at index 0 because it is split by the `|`,
            # afterwards the `Clone1` is at index 1 because it is between the `CloneId=` and the next `|`.
            index=1,
            target_tag_id=TagId(1337)  # Use the tag ID you want to store the clone ID in
        )
        ```

    """
    index: int
    """The index of the split to use as the clone ID.
    Since this is an index, it is 0-based. So the first item is at index 0, the second at index 1, etc.
    """
    target_tag_id: TagId
    """The tag to store the extracted clone ID in."""

    def to_api_payload(self) -> openapi_client.CloneIdToTagSpec:
        return openapi_client.CloneIdToTagSpec(
            source=self.source,
            delimiter=self.delimiter if isinstance(self.delimiter, str) else "/".join(self.delimiter),
            index=self.index,
            target_tag_id=self.target_tag_id,
        )


class CorrectionRegion(str, Enum):
    FR1 = "FR1"
    CDR1 = "CDR1"
    FR2 = "FR2"
    CDR2 = "CDR2"
    FR3 = "FR3"
    FR4 = "FR4"


class CorrectionSettings(BaseModel):
    """The settings to correct or complete regions of sequences.

    Example:

        To complete the FR1 and FR4 regions and correct all regions (except CDR3 that is not a region that can be configured to be corrected),
        you can use the following `CorrectionSettings` configuration:

        ```python
        CorrectionSettings(
            should_complete_ends=True,
            regions=[
                CorrectionRegion.FR1,
                CorrectionRegion.CDR1,
                CorrectionRegion.FR2,
                CorrectionRegion.CDR2,
                CorrectionRegion.FR3,
                CorrectionRegion.FR4,
            ],
        )
        ```
    """

    should_complete_ends: bool
    """Whether to complete FR1 and FR4 region of sequences."""
    regions: list[CorrectionRegion]
    """The names of the regions to correct"""

    def to_api_payload(self) -> openapi_client.CorrectionSettings:
        return openapi_client.CorrectionSettings(should_complete_ends=self.should_complete_ends, regions=[i.value for i in self.regions])
