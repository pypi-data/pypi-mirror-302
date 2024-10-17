from enum import Enum
from typing import NewType

from igx_api.l1 import openapi_client
from igx_api.l2.types.cluster import ClusterId, ClusterRunId
from igx_api.l2.util.from_raw_model import FromRawModel

TreeId = NewType("TreeId", int)
"""The unique identifier of a set of nucleotide/amino acid trees"""


class TreeType(str, Enum):
    NUCLEOTIDE = "nucleotide"
    AMINO_ACID = "amino_acid"


class Tree(FromRawModel[openapi_client.Tree]):
    cluster_run_id: ClusterRunId
    cluster_id: ClusterId
    tree_id: TreeId
    newick: str
    type: TreeType

    @classmethod
    def _build(cls, raw: openapi_client.Tree) -> "Tree":
        return cls(
            cluster_run_id=ClusterRunId(raw.cluster_run_id),
            cluster_id=ClusterId(int(raw.cluster_id)),
            tree_id=TreeId(int(raw.tree_id)),
            newick=raw.newick,
            type=TreeType.NUCLEOTIDE if raw.type == "nucleotide" else TreeType.AMINO_ACID,
        )


class StartTreeResultPayload(FromRawModel[openapi_client.GetTrees]):
    cluster_run_id: ClusterRunId
    cluster_id: ClusterId
    tree_id: TreeId

    @classmethod
    def _build(cls, raw: openapi_client.GetTrees) -> "StartTreeResultPayload":
        return cls(
            cluster_run_id=ClusterRunId(raw.cluster_run_id),
            cluster_id=ClusterId(int(raw.cluster_id)),
            tree_id=TreeId(int(raw.tree_id)),
        )
