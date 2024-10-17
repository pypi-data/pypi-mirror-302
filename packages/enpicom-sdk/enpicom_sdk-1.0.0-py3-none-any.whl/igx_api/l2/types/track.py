from datetime import datetime
from enum import Enum
from typing import Literal, NewType

from pydantic import BaseModel
from typing_extensions import assert_never

from igx_api.l1 import openapi_client
from igx_api.l2.types.cluster import ClusterRunId
from igx_api.l2.types.collection import CollectionId
from igx_api.l2.util.from_raw_model import FromRawModel

TrackRunId = NewType("TrackRunId", int)
"""The unique identifier of a Track run"""

TrackTemplateId = NewType("TrackTemplateId", int)
"""The unique identifier of a Track Template"""


class TrackOperationType(str, Enum):
    """Types of operations available in Track."""

    UNION = "union"
    INTERSECTION = "intersection"
    DIFFERENCE = "difference"
    FOLD_CHANGE = "fold_change"


class SimplifiedTrackOperation(BaseModel):
    """Simplified read model for Track Operation.

    Attributes:
        name (str): Operation name.
        type (TrackOperationTypes): Operation type.
    """

    name: str
    type: TrackOperationType


class SimplifiedTrackTemplate(BaseModel):
    """Simplified read model for Track Template.

    Attributes:
        id (TrackTemplateId): Track Template Id.
        name (str): Operation name.
        created_at (datetime): Date when the template was created.
    """

    id: TrackTemplateId
    name: str
    created_at: datetime


class TrackRun(FromRawModel[openapi_client.ExistingTrackRun]):
    """Existing Track Run configuration.

    Attributes:
        id (TrackRunId): Track Run Id.
        name (str): Track Run name.
        template_id (TrackTemplateId): Track Template Id.
        cluster_run_id (ClusterRunId): Cluster Run Id.
        created_at (datetime): Cluster Run creation date.
        operations (list[SimplifiedTrackOperation]): List of operations present in this Track run.
    """

    id: TrackRunId
    name: str
    template_id: TrackTemplateId
    cluster_run_id: ClusterRunId
    operations: list[SimplifiedTrackOperation]

    @classmethod
    def _build(cls, raw: openapi_client.ExistingTrackRun) -> "TrackRun":
        return cls(
            id=TrackRunId(raw.id),
            name=str(raw.name),
            template_id=TrackTemplateId(raw.template_id),
            cluster_run_id=ClusterRunId(raw.cluster_run_id),
            operations=[SimplifiedTrackOperation(name=d.name, type=d.type) for d in raw.operations],
        )


class TrackTemplateFoldChangeInputOperations(BaseModel):
    from_operation: str | None = None
    to_operation: str | None = None


class TrackTemplateFoldChangeAnnotation(FromRawModel[openapi_client.TrackTemplateFoldChangeAnnotation]):
    name: str
    input_operations: TrackTemplateFoldChangeInputOperations | None = None

    @classmethod
    def _build(cls, raw: openapi_client.TrackTemplateFoldChangeAnnotation) -> "TrackTemplateFoldChangeAnnotation":
        return cls(
            name=str(raw.name),
            input_operations=TrackTemplateFoldChangeInputOperations(
                from_operation=raw.inputs.var_from,
                to_operation=raw.inputs.to,
            )
            if raw.inputs is not None
            else None,
        )


class TrackTemplateUnionOperation(FromRawModel[openapi_client.TrackTemplateJoinOperation]):
    name: str
    input_operations: list[str] | None = None
    annotations: list[TrackTemplateFoldChangeAnnotation] | None = None

    @classmethod
    def _build(cls, raw: openapi_client.TrackTemplateJoinOperation) -> "TrackTemplateUnionOperation":
        return cls(
            name=str(raw.name),
            input_operations=[str(x) for x in raw.inputs],
            annotations=[TrackTemplateFoldChangeAnnotation.from_raw(x) for x in raw.annotations] if raw.annotations is not None else None,
        )


class TrackTemplateIntersectionOperation(FromRawModel[openapi_client.TrackTemplateJoinOperation]):
    name: str
    input_operations: list[str] | None = None
    annotations: list[TrackTemplateFoldChangeAnnotation] | None = None

    @classmethod
    def _build(cls, raw: openapi_client.TrackTemplateJoinOperation) -> "TrackTemplateIntersectionOperation":
        return cls(
            name=str(raw.name),
            input_operations=[str(x) for x in raw.inputs],
            annotations=[TrackTemplateFoldChangeAnnotation.from_raw(x) for x in raw.annotations] if raw.annotations is not None else None,
        )


class TrackTemplateDifferenceInputs(BaseModel):
    remove_operation: str | None = None
    from_operation: str | None = None


class TrackTemplateDifferenceOperation(FromRawModel[openapi_client.TrackTemplateDifferenceOperation]):
    name: str
    input_operations: TrackTemplateDifferenceInputs | None = None
    annotations: list[TrackTemplateFoldChangeAnnotation] | None = None

    @classmethod
    def _build(cls, raw: openapi_client.TrackTemplateDifferenceOperation) -> "TrackTemplateDifferenceOperation":
        return cls(
            name=str(raw.name),
            input_operations=TrackTemplateDifferenceInputs(
                remove_operation=raw.inputs.remove,
                from_operation=raw.inputs.var_from,
            ),
            annotations=[TrackTemplateFoldChangeAnnotation.from_raw(x) for x in raw.annotations] if raw.annotations is not None else None,
        )


TrackTemplateOperation = TrackTemplateUnionOperation | TrackTemplateIntersectionOperation | TrackTemplateDifferenceOperation


class ExistingTrackTemplate(FromRawModel[openapi_client.ExistingTrackTemplate]):
    """Track Template configuration.

    Attributes:
        id: (TrackTemplateId): Track Template Id
        name (str): Track Template name.
        created_at (datetime): Date of the Template's creation.
        operations (list[TrackOperation]): List of operations present in this Track run.
    """

    id: TrackTemplateId
    name: str
    created_at: datetime
    operations: list[TrackTemplateOperation]

    @classmethod
    def _build(cls, raw: openapi_client.ExistingTrackTemplate) -> "ExistingTrackTemplate":
        return cls(
            id=TrackTemplateId(raw.id),
            name=str(raw.name),
            created_at=raw.created_at,
            operations=[build_operation(d) for d in raw.operations],
        )


def transform_operation(op: TrackTemplateOperation) -> openapi_client.TrackTemplateTrackOperation:
    annotations = (
        [
            openapi_client.TrackTemplateFoldChangeAnnotation(
                name=x.name,
                type=TrackOperationType.FOLD_CHANGE,
                inputs=openapi_client.TrackTemplateFoldChangeAnnotationInputs(
                    **{
                        "from": x.input_operations.from_operation if x.input_operations is not None else None,
                        "to": x.input_operations.to_operation if x.input_operations is not None else None,
                    }
                ),
            )
            for x in op.annotations
        ]
        if op.annotations is not None
        else None
    )

    if isinstance(op, TrackTemplateUnionOperation):
        return openapi_client.TrackTemplateTrackOperation(
            openapi_client.TrackTemplateJoinOperation(
                name=op.name,
                type=TrackOperationType.UNION,
                inputs=op.input_operations if op.input_operations is not None else [],
                annotations=annotations,
            )
        )
    elif isinstance(op, TrackTemplateIntersectionOperation):
        return openapi_client.TrackTemplateTrackOperation(
            openapi_client.TrackTemplateJoinOperation(
                name=op.name,
                type=TrackOperationType.INTERSECTION,
                inputs=op.input_operations if op.input_operations is not None else [],
                annotations=annotations,
            )
        )
    elif isinstance(op, TrackTemplateDifferenceOperation):
        return openapi_client.TrackTemplateTrackOperation(
            openapi_client.TrackTemplateDifferenceOperation(
                name=op.name,
                type=TrackOperationType.DIFFERENCE,
                inputs=openapi_client.TrackTemplateDifferenceOperationInputs(
                    **{
                        "remove": op.input_operations.remove_operation if op.input_operations is not None else None,
                        "from": op.input_operations.from_operation if op.input_operations is not None else None,
                    }
                ),
                annotations=annotations,
            )
        )
    else:
        raise ValueError("Wrong Track operation type")


def build_operation(op: openapi_client.TrackTemplateTrackOperation) -> TrackTemplateOperation:
    if isinstance(op.actual_instance, openapi_client.TrackTemplateJoinOperation):
        if op.actual_instance.type == TrackOperationType.UNION:
            return TrackTemplateUnionOperation.from_raw(op.actual_instance)
        else:
            return TrackTemplateIntersectionOperation.from_raw(op.actual_instance)
    elif isinstance(op.actual_instance, openapi_client.TrackTemplateDifferenceOperation):
        return TrackTemplateDifferenceOperation.from_raw(op.actual_instance)
    else:
        raise ValueError("Wrong Track operation type")


class CollectionSelector(BaseModel):
    type: Literal["collection_id"] | None = "collection_id"
    value: CollectionId


class UnionOperationInput(BaseModel):
    name: str
    input_collections: list[CollectionSelector]


class IntersectionOperationInput(BaseModel):
    name: str
    input_collections: list[CollectionSelector]


class DifferenceOperationInputCollections(BaseModel):
    remove_collection: CollectionSelector | None = None
    from_collection: CollectionSelector | None = None


class DifferenceOperationInput(BaseModel):
    name: str
    input_collections: DifferenceOperationInputCollections | None = None


class FoldChangeInputCollections(BaseModel):
    from_collection: CollectionSelector | None = None
    to_collection: CollectionSelector | None = None


class FoldChangeInput(BaseModel):
    name: str
    input_collections: FoldChangeInputCollections | None = None


TrackWorkInput = UnionOperationInput | IntersectionOperationInput | DifferenceOperationInput | FoldChangeInput


def transform_collection_selector(sel: CollectionSelector) -> openapi_client.MatchCollectionByItsID:
    if isinstance(sel, CollectionSelector):
        return openapi_client.MatchCollectionByItsID(type="collection_id", value=int(sel.value))
    else:
        assert_never(sel)


def transform_operation_input(input: TrackWorkInput) -> openapi_client.TrackWorkInputsInner:
    if isinstance(input, UnionOperationInput):
        return openapi_client.TrackWorkInputsInner(
            openapi_client.JoinOperationInputs(
                name=input.name,
                type=TrackOperationType.UNION,
                inputs=[openapi_client.JoinOperationInputsInputsInner(transform_collection_selector(x)) for x in input.input_collections],
            )
        )
    elif isinstance(input, IntersectionOperationInput):
        return openapi_client.TrackWorkInputsInner(
            openapi_client.JoinOperationInputs(
                name=input.name,
                type=TrackOperationType.INTERSECTION,
                inputs=[openapi_client.JoinOperationInputsInputsInner(transform_collection_selector(x)) for x in input.input_collections],
            )
        )
    elif isinstance(input, DifferenceOperationInput):
        return openapi_client.TrackWorkInputsInner(
            openapi_client.DifferenceOperationInputs(
                name=input.name,
                type=TrackOperationType.DIFFERENCE,
                inputs=openapi_client.DifferenceOperationInputsInputs(
                    **{
                        "remove": openapi_client.DifferenceOperationInputsInputsRemove(transform_collection_selector(input.input_collections.remove_collection))
                        if input.input_collections is not None and input.input_collections.remove_collection is not None
                        else None,
                        "from": openapi_client.DifferenceOperationInputsInputsRemove(transform_collection_selector(input.input_collections.from_collection))
                        if input.input_collections is not None and input.input_collections.from_collection is not None
                        else None,
                    }
                ),
            )
        )
    elif isinstance(input, FoldChangeInput):
        return openapi_client.TrackWorkInputsInner(
            openapi_client.FoldChangeAnnotationInputs(
                name=input.name,
                type=TrackOperationType.FOLD_CHANGE,
                inputs=openapi_client.FoldChangeAnnotationInputsInputs(
                    **{
                        "from": openapi_client.DifferenceOperationInputsInputsRemove(transform_collection_selector(input.input_collections.from_collection))
                        if input.input_collections is not None and input.input_collections.from_collection is not None
                        else None,
                        "to": openapi_client.DifferenceOperationInputsInputsRemove(transform_collection_selector(input.input_collections.to_collection))
                        if input.input_collections is not None and input.input_collections.to_collection is not None
                        else None,
                    }
                ),
            )
        )
    else:
        assert_never(input)


class TrackExportMode(str, Enum):
    RESULTS = "results"
    REPRESENTATIVES = "representatives"
    CONSENSUS = "consensus"
