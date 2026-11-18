from datetime import datetime, timezone
from enum import StrEnum
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field


class Severity(StrEnum):
    LOW = 'low'
    MEDIUM = 'medium'
    HIGH = 'high'
    CRITICAL = 'critical'


class IncidentStatus(StrEnum):
    OPEN = 'open'
    UNDER_REVIEW = 'under_review'
    CLOSED = 'closed'


class Finding(BaseModel):
    model_config = ConfigDict(extra='forbid')
    description: str = Field(min_length=5)
    event_ids: list[str] = Field(min_length=1)


class Reference(BaseModel):
    model_config = ConfigDict(extra='forbid')
    title: str
    url: str  # Validated as a string so offline references may be omitted entirely.


class IncidentReport(BaseModel):
    model_config = ConfigDict(extra='forbid')

    id: UUID = Field(default_factory=uuid4)
    scenario_id: str = Field(min_length=1)
    title: str = Field(min_length=5)
    summary: str = Field(min_length=15)
    severity: Severity
    status: IncidentStatus = IncidentStatus.UNDER_REVIEW
    confidence: float = Field(ge=0.0, le=1.0)
    findings: list[Finding] = Field(min_length=1)
    affected_assets: list[str] = Field(default_factory=list)
    recommendations: list[str] = Field(min_length=1)
    external_references: list[Reference] = Field(default_factory=list)
    requires_human_review: bool = True
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
