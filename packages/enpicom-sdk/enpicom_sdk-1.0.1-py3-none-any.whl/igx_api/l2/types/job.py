from enum import Enum
from typing import NewType, Self

from igx_api.l1 import openapi_client
from igx_api.l2.util.from_raw_model import FromRawModel, RawType

JobId = NewType("JobId", int)
"""The unique identifier of a job."""


class JobState(str, Enum):
    """Current state of a job."""

    QUEUED = "queued"
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    CANCELLED = "cancelled"
    FAILED = "failed"
    TIMED_OUT = "timed_out"


class Job(FromRawModel[openapi_client.GetJob200ResponseJob]):
    """A single job representing a long-running task, e.g. an app run."""

    id: JobId
    """The unique identifier of a job."""
    state: JobState
    """Current state of a job."""

    @classmethod
    def _build(cls, raw: RawType) -> Self:
        return cls(
            id=JobId(raw.id),
            state=JobState(raw.state),
        )
