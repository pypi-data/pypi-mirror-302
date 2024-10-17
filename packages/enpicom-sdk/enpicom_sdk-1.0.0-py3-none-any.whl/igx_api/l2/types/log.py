from enum import Enum

from pydantic import BaseModel


class LogLevel(str, Enum):
    Trace = "TRACE"
    Debug = "DEBUG"
    Info = "INFO"
    Success = "SUCCESS"
    Warning = "WARNING"
    Error = "ERROR"
    Critical = "CRITICAL"


class LogLevelModel(BaseModel):
    level: LogLevel
