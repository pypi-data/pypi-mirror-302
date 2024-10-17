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
"""The unique identifier of a Track Run."""

TrackTemplateId = NewType("TrackTemplateId", int)
"""The unique identifier of a Track Template."""


class TrackOperationType(str, Enum):
    """Types of operations available in Track."""

    UNION = "union"
    INTERSECTION = "intersection"
    DIFFERENCE = "difference"
    FOLD_CHANGE = "fold_change"


class SimplifiedTrackOperation(BaseModel):
    """Simplified read model for Track Operation."""

    name: str
    """Operation name."""
    type: TrackOperationType
    """Operation type."""


class SimplifiedTrackTemplate(BaseModel):
    """Simplified read model for Track Template."""

    id: TrackTemplateId
    """Track Template Id."""
    name: str
    """Operation name."""
    created_at: datetime
    """Date when the template was created."""


class TrackRun(FromRawModel[openapi_client.ExistingTrackRun]):
    """Existing Track Run configuration."""

    id: TrackRunId
    """Track Run Id."""
    name: str
    """Track Run name."""
    template_id: TrackTemplateId
    """Track Template Id."""
    cluster_run_id: ClusterRunId
    """Cluster Run Id."""
    operations: list[SimplifiedTrackOperation]
    """List of operations present in this Track run."""

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
    """Track Fold change input operations that can be specified within the Track template.

    The results of the operations specified for this object will be used as inputs
    for the fold change measeurement computation.

    Example:
        Fold change ratio between results "A" and "B" after operation "C" is done equals 2.
    """

    from_operation: str | None = None
    """Previously computed operation results or input clone collections.
        Serves as the `B` value in the `A`/`B` fold change ratio formula."""
    to_operation: str | None = None
    """Previously computed operation results or input clone collections.
        Serves as the `A` value in the `A`/`B` fold change ratio formula."""


class TrackTemplateFoldChangeAnnotation(FromRawModel[openapi_client.TrackTemplateFoldChangeAnnotation]):
    """Track fold change annotation computed for input operations results, defined within a Track template."""

    name: str
    """Name of the fold change annotation annotation. Has to be unique."""
    input_operations: TrackTemplateFoldChangeInputOperations | None = None
    """Fold change input operations, a results of previously planned (performed during Track run) operations within the template."""

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
    """Definition of a Track union operation performed on the results of provided operations."""

    name: str
    """Name of the union operation. Has to be unique."""
    input_operations: list[str] | None = None
    """A list of input operations for results of which the union will be applied."""
    annotations: list[TrackTemplateFoldChangeAnnotation] | None = None
    """Optional annotations to be added onto this operation result."""

    @classmethod
    def _build(cls, raw: openapi_client.TrackTemplateJoinOperation) -> "TrackTemplateUnionOperation":
        return cls(
            name=str(raw.name),
            input_operations=[str(x) for x in raw.inputs],
            annotations=[TrackTemplateFoldChangeAnnotation.from_raw(x) for x in raw.annotations] if raw.annotations is not None else None,
        )


class TrackTemplateIntersectionOperation(FromRawModel[openapi_client.TrackTemplateJoinOperation]):
    """Definition of a Track intersection operation performed on the results of provided operations."""

    name: str
    """Name of the intersection operation. Has to be unique."""
    input_operations: list[str] | None = None
    """A list of input operations for results of which the intersection will be applied."""
    annotations: list[TrackTemplateFoldChangeAnnotation] | None = None
    """Optional annotations to be added onto this operation result."""

    @classmethod
    def _build(cls, raw: openapi_client.TrackTemplateJoinOperation) -> "TrackTemplateIntersectionOperation":
        return cls(
            name=str(raw.name),
            input_operations=[str(x) for x in raw.inputs],
            annotations=[TrackTemplateFoldChangeAnnotation.from_raw(x) for x in raw.annotations] if raw.annotations is not None else None,
        )


class TrackTemplateDifferenceInputs(BaseModel):
    """Track difference operation inputs that can be specified within
    the Track template.

    Example:
        Assuming two operations `Operation A` and `Operation B` were already specified in the Track template:

        ```python
        # A difference operation specified in the Track template
        TrackTemplateDifferenceOperation(
            name="Operation C",
            input_operations=TrackTemplateDifferenceInputs(
                remove_operation="Operation A",
                from_operation="Operation B",
            ),
        ),
        ```
    """

    remove_operation: str | None = None
    """Clusters from this operation will be subtracted from the other one."""
    from_operation: str | None = None
    """Clusters from the other operation result will be subtracted from this one."""


class TrackTemplateDifferenceOperation(FromRawModel[openapi_client.TrackTemplateDifferenceOperation]):
    """Definition of a Track difference operation performed on the results of provided operations."""

    name: str
    """Name of the difference operation. Has to be unique."""
    input_operations: TrackTemplateDifferenceInputs | None = None
    """Track difference operation inputs that can be specified within the Track template."""
    annotations: list[TrackTemplateFoldChangeAnnotation] | None = None
    """Optional annotations to be added onto this operation result."""

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
"""A single Track operation definition present in the Track template.

    In general, those are used to to define what operations will be performed during the Track run.
    They need to have unique names (for matching purposes) and either need other operations within the template to be specified
    as their inputs or have inputs matched with them later on via `igx_api.l2.types.track.TrackWorkInput`.
"""


class ExistingTrackTemplate(FromRawModel[openapi_client.ExistingTrackTemplate]):
    """Track Template configuration."""

    id: TrackTemplateId
    """The unique identifier of a Track Template."""
    name: str
    """Name of a Track Template."""
    created_at: datetime
    """Date of the Track Template's creation."""
    operations: list[TrackTemplateOperation]
    """List of operations present in this Track Run."""

    @classmethod
    def _build(cls, raw: openapi_client.ExistingTrackTemplate) -> "ExistingTrackTemplate":
        return cls(
            id=TrackTemplateId(raw.id),
            name=str(raw.name),
            created_at=raw.created_at,
            operations=[build_operation(d) for d in raw.operations],
        )


def transform_operation(op: TrackTemplateOperation) -> openapi_client.TrackTemplateTrackOperation:
    """An internal function used for transforming Track template operations config into API format.
    @private

    Args:
        op (TrackTemplateOperation): Track template operation in "user format".

    Returns:
        openapi_client.TrackTemplateTrackOperation: Track template in "API format".
    """
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
    """An internal function used for transforming Track template operations config from API format to "user format".
    @private

    Args:
        op (openapi_client.TrackTemplateTrackOperation): Track template operation in "API format".

    Returns:
        TrackTemplateOperation: Track template in "user format".
    """
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
    """Selects a collection by matching it with the provided unique ID."""

    type: Literal["collection_id"] | None = "collection_id"
    """Internal type used to recognize the selector object."""
    value: CollectionId
    """The unique identifier of a collection."""


class UnionOperationInput(BaseModel):
    """Used to specify input collections for union operation during Track run configuration."""

    name: str
    """Name of the union operation. Has to match the one defined in the Track template."""
    input_collections: list[CollectionSelector]
    """A list of input clone collections."""


class IntersectionOperationInput(BaseModel):
    """Used to specify input collections for intersection operation during Track run configuration."""

    name: str
    """Name of the intersection operation. Has to match the one defined in the Track template."""
    input_collections: list[CollectionSelector]
    """A list of input clone collections."""


class DifferenceOperationInputCollections(BaseModel):
    """Used to specify input collections for difference operation during Track run configuration."""

    remove_collection: CollectionSelector | None = None
    """Clusters from this collection will be removed from the other one."""
    from_collection: CollectionSelector | None = None
    """Clusters from the other collection will be removed from this one."""


class DifferenceOperationInput(BaseModel):
    """Used to specify input collections for intersection operation during Track run configuration."""

    name: str
    """Name of the intersection operation. Has to match the one defined in the Track template."""
    input_collections: DifferenceOperationInputCollections | None = None
    """Used to specify input collections for difference operation during Track run configuration."""


class FoldChangeInputCollections(BaseModel):
    """Track Fold change input operations that can be specified during the Track run configuration.

    The clone collection inputs specified for this object will be used as inputs
    for the fold change measeurement computation.

    Example:
        Fold change ratio between results "A" and "B" after operation "C" is done equals 2.
    """

    from_collection: CollectionSelector | None = None
    """An input clone collection.
        Serves as the `B` value in the `A`/`B` fold change ratio formula."""
    to_collection: CollectionSelector | None = None
    """An input clone collection.
        Serves as the `A` value in the `A`/`B` fold change ratio formula."""


class FoldChangeInput(BaseModel):
    """Track fold change annotation specification."""

    name: str
    """Name of the fold change annotation annotation. Has to match the one defined in the Track template."""
    input_collections: FoldChangeInputCollections | None = None
    """Input collections for the fold change."""


TrackWorkInput = UnionOperationInput | IntersectionOperationInput | DifferenceOperationInput | FoldChangeInput
"""An input for Track run configuration, used to provide data for the operations and annotations specified
    previously within the Track template configuration.

    In general, they need to match the unique names specified within Track templates in order to fill them
    with the clustered clone data - for info about the templates, see `igx_api.l2.types.track.TrackTemplateOperation`.
"""


def transform_collection_selector(sel: CollectionSelector) -> openapi_client.MatchCollectionByItsID:
    """Internal transform function for collection selectors.
    @private
    """
    if isinstance(sel, CollectionSelector):
        return openapi_client.MatchCollectionByItsID(type="collection_id", value=int(sel.value))
    else:
        assert_never(sel)


def transform_operation_input(input: TrackWorkInput) -> openapi_client.TrackWorkInputsInner:
    """Internal transform function for operation inputs.
    @private
    """
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
    """Mode of Track export that determines the shape and content of the final file."""

    RESULTS = "results"
    """All clones from each cluster will be exported."""
    REPRESENTATIVES = "representatives"
    """Within each cluster, every unique CDR/FR sequence will be tallied and the most abundant sequence for each region will be chosen."""
    CONSENSUS = "consensus"
    """The clone abundance will be used to choose a representative from each cluster."""
