from enum import Enum
from typing import NewType

from igx_api.l1 import openapi_client
from igx_api.l2.types.sequence import Chain
from igx_api.l2.types.tag import TagId
from igx_api.l2.types.user import UserId
from igx_api.l2.util.from_raw_model import FromRawModel

BasketId = NewType("BasketId", int)
"""Unique identifier of a Basket."""


class Basket(FromRawModel[openapi_client.Basket]):
    """A single Basket info."""

    id: BasketId
    """Unique identifier of a Basket."""
    name: str
    """Name of a Basket."""
    shared: bool
    """Determines if a Basket is visible to other users in the organization."""
    user_id: UserId
    """Unique identifier of a user which created given Basket."""

    @classmethod
    def _build(cls, raw: openapi_client.Basket) -> "Basket":
        return cls(
            id=BasketId(raw.id),
            name=str(raw.name),
            shared=bool(raw.shared),
            user_id=UserId(raw.user_id),
        )


class BasketExportFormat(str, Enum):
    """Format of the result file of a Basket clones export."""

    TSV = "tsv"
    FASTA = "fasta"


class FastaExportHeadersConfig(FromRawModel[openapi_client.StartFastaClonesExportRequestBodyFastaConfigHeaders]):
    """Configuration of the FASTA sequence headers that are written in Basket FASTA export flow."""

    include_unique_clone_id: bool
    """Determines if clone IDs will be included in the FASTA sequence headers."""
    include_unique_sequence_id: bool
    """Determines if sequence IDs will be included in the FASTA sequence headers."""
    include_chain: bool
    """Determines if sequence Chain Tag will be included in FASTA sequence headers."""
    tags: list[TagId]
    """Unique identifiers of tags that are meant to be included in FASTA sequence headers."""

    @classmethod
    def _build(cls, raw: openapi_client.StartFastaClonesExportRequestBodyFastaConfigHeaders) -> "FastaExportHeadersConfig":
        return cls(
            include_unique_clone_id=raw.include_unique_clone_id,
            include_unique_sequence_id=raw.include_unique_sequence_id,
            include_chain=raw.include_chain,
            tags=[TagId(tag_id) for tag_id in raw.tags],
        )

    def to_api_payload(self) -> openapi_client.models.StartFastaClonesExportRequestBodyFastaConfigHeaders:
        return openapi_client.models.StartFastaClonesExportRequestBodyFastaConfigHeaders(
            include_unique_clone_id=self.include_unique_clone_id,
            include_unique_sequence_id=self.include_unique_sequence_id,
            include_chain=self.include_chain,
            tags=[int(tag_id) for tag_id in self.tags],
        )


class FastaExportSequenceRegion(str, Enum):
    """A subset of sequence region Tags that are allowed as input in FASTA sequence configuration.
    Enum values are not written in snake_case notation on purpose, they must match the exact values
    held by Tag Archetypes in the IGX-Platform."""

    FR1_NUCLEOTIDES = "FR1 Nucleotides"
    FR2_NUCLEOTIDES = "FR2 Nucleotides"
    FR3_NUCLEOTIDES = "FR3 Nucleotides"
    FR4_NUCLEOTIDES = "FR4 Nucleotides"
    CDR1_NUCLEOTIDES = "CDR1 Nucleotides"
    CDR2_NUCLEOTIDES = "CDR2 Nucleotides"
    CDR3_NUCLEOTIDES = "CDR3 Nucleotides"
    RECEPTOR_NUCLEOTIDES = "Receptor Nucleotides"
    FR1_AMINO_ACIDS = "FR1 Amino Acids"
    FR2_AMINO_ACIDS = "FR2 Amino Acids"
    FR3_AMINO_ACIDS = "FR3 Amino Acids"
    FR4_AMINO_ACIDS = "FR4 Amino Acids"
    CDR1_AMINO_ACIDS = "CDR1 Amino Acids"
    CDR2_AMINO_ACIDS = "CDR2 Amino Acids"
    CDR3_AMINO_ACIDS = "CDR3 Amino Acids"
    RECEPTOR_AMINO_ACIDS = "Receptor Amino Acids"


class FastaExportSequences(FromRawModel[openapi_client.StartFastaClonesExportRequestBodyFastaConfigSequences]):
    """
    Configuration of the sequences in the exported FASTA file. In case of multiple sequence regions being
    specified for a single chain, sequence values for said chain will be concatenated without any separators
    in the exported file."""

    Heavy: list[FastaExportSequenceRegion] | None = None
    Lambda: list[FastaExportSequenceRegion] | None = None
    Kappa: list[FastaExportSequenceRegion] | None = None
    Alpha: list[FastaExportSequenceRegion] | None = None
    Beta: list[FastaExportSequenceRegion] | None = None
    Gamma: list[FastaExportSequenceRegion] | None = None
    Delta: list[FastaExportSequenceRegion] | None = None
    Iota: list[FastaExportSequenceRegion] | None = None

    @classmethod
    def _build(cls, raw: openapi_client.StartFastaClonesExportRequestBodyFastaConfigSequences) -> "FastaExportSequences":
        return cls(
            Heavy=[FastaExportSequenceRegion(region) for region in raw.heavy] if raw.heavy is not None else None,
            Kappa=[FastaExportSequenceRegion(region) for region in raw.kappa] if raw.kappa is not None else None,
            Lambda=[FastaExportSequenceRegion(region) for region in raw.var_lambda] if raw.var_lambda is not None else None,
            Alpha=[FastaExportSequenceRegion(region) for region in raw.alpha] if raw.alpha is not None else None,
            Beta=[FastaExportSequenceRegion(region) for region in raw.beta] if raw.beta is not None else None,
            Gamma=[FastaExportSequenceRegion(region) for region in raw.gamma] if raw.gamma is not None else None,
            Delta=[FastaExportSequenceRegion(region) for region in raw.delta] if raw.delta is not None else None,
            Iota=[FastaExportSequenceRegion(region) for region in raw.iota] if raw.iota is not None else None,
        )

    def to_api_payload(self) -> openapi_client.models.StartFastaClonesExportRequestBodyFastaConfigSequences:
        return openapi_client.StartFastaClonesExportRequestBodyFastaConfigSequences(
            **{
                "heavy": [region.value for region in self.Heavy] if self.Heavy is not None else None,
                "kappa": [region.value for region in self.Kappa] if self.Kappa is not None else None,
                "lambda": [region.value for region in self.Lambda] if self.Lambda is not None else None,
                "alpha": [region.value for region in self.Alpha] if self.Alpha is not None else None,
                "beta": [region.value for region in self.Beta] if self.Beta is not None else None,
                "gamma": [region.value for region in self.Gamma] if self.Gamma is not None else None,
                "delta": [region.value for region in self.Delta] if self.Delta is not None else None,
                "iota": [region.value for region in self.Iota] if self.Iota is not None else None,
            }
        )


class FastaExportConfig(FromRawModel[openapi_client.StartFastaClonesExportRequestBodyFastaConfig]):
    """Full configuration of Basket FASTA export."""

    headers: FastaExportHeadersConfig
    """The configuration of FASTA sequence headers."""
    sequences: FastaExportSequences
    """Entries representing sequences (lines) written in the FASTA file."""

    @classmethod
    def _build(cls, raw: openapi_client.StartFastaClonesExportRequestBodyFastaConfig) -> "FastaExportConfig":
        return cls(
            headers=FastaExportHeadersConfig.from_raw(raw.headers),
            sequences=FastaExportSequences.from_raw(raw.sequences),
        )

    def to_api_payload(self) -> openapi_client.models.StartFastaClonesExportRequestBodyFastaConfig:
        return openapi_client.models.StartFastaClonesExportRequestBodyFastaConfig(
            headers=self.headers.to_api_payload(),
            sequences=self.sequences.to_api_payload(),
        )


def fasta_config(
    sequences: dict[Chain, list[FastaExportSequenceRegion]],
    include_chain_header: bool = True,
    include_unique_clone_id_header: bool = True,
    include_unique_sequence_id_header: bool = False,
    header_tags: list[TagId] = [],
) -> FastaExportConfig:
    """A utility function used for building a Basket FASTA export configuration from user input.

    Args:
        include_unique_clone_id_header (bool): determines if Unique Clone Identifier will be included in FASTA sequence headers.
        include_unique_sequence_id_header (bool): determines if Unique Sequence Identifier will be included in FASTA sequence headers.
        include_chain_header (bool): determines if sequence Chain will be included in FASTA sequence headers.
        header_tags (list[TagId]): tags that are meant to be included in FASTA sequence headers, they will be displayed with their key and their value.
        sequences (dict[Chain, list[FastaExportSequenceRegion]): entries representing sequences (lines) written in the FASTA file:
            e.g. in case of two clones, each with a heavy sequence, a `{Chain.HEAVY: [FastaExportSequenceRegion.CDR3_AMINO_ACIDS]}`
            object will result in two lines written in the FASTA file. Specifying multiple sequence regions for a single Chain will
            result in concatenation of those sequences.
    """

    return FastaExportConfig(
        headers=FastaExportHeadersConfig(
            include_unique_clone_id=include_unique_clone_id_header,
            include_unique_sequence_id=include_unique_sequence_id_header,
            include_chain=include_chain_header,
            tags=header_tags,
        ),
        sequences=FastaExportSequences(
            Alpha=sequences.get(Chain.ALPHA),
            Beta=sequences.get(Chain.BETA),
            Delta=sequences.get(Chain.DELTA),
            Gamma=sequences.get(Chain.GAMMA),
            Heavy=sequences.get(Chain.HEAVY),
            Iota=sequences.get(Chain.IOTA),
            Kappa=sequences.get(Chain.KAPPA),
            Lambda=sequences.get(Chain.LAMBDA),
        ),
    )
