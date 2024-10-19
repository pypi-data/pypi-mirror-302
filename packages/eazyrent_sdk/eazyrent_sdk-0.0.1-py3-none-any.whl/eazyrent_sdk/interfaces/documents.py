from datetime import datetime, timezone
from typing import Any, List
from uuid import UUID, uuid4

from pydantic import AwareDatetime, BaseModel, Field

from .alerts import Alert
from .types import DOCUMENT_STATUS


class DocumentSlice(BaseModel):
    file: UUID
    pages: List[int] = []


class Document(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    status: DOCUMENT_STATUS = Field(default="RECEIVED")
    document_type: UUID = Field(...)
    alerts: List[Alert] = Field([])
    document_model: str | None = Field(None)
    extraction_results: Any = Field(default=None)
    created_at: AwareDatetime = Field(
        default_factory=lambda: datetime.now(tz=timezone.utc)
    )
    updated_at: AwareDatetime | None = Field(None)
    files: List[DocumentSlice] = []
    meta: Any = None
