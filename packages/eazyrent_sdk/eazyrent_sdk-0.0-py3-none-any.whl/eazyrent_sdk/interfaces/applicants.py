from datetime import datetime, timezone
from pathlib import Path
from typing import Any, List
from uuid import UUID, uuid4

from pydantic import AwareDatetime, BaseModel, EmailStr, Field

from .documents import Document
from .types import APPLICANT_STATUS


class MoralGuarantor(BaseModel):
    file_path: Path
    type: str
    created_at: AwareDatetime
    updated_at: AwareDatetime


class Applicant(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    status: APPLICANT_STATUS = Field(default="NEW")
    first_name: str | None = Field(None)
    last_name: str | None = Field(None)
    email: EmailStr | None = Field(None)
    phone: str | None = Field(None)
    form_submitted: AwareDatetime | None = Field(None)
    score: float | None = Field(None)
    created_at: AwareDatetime = Field(
        default_factory=lambda: datetime.now(tz=timezone.utc)
    )
    updated_at: AwareDatetime | None = Field(None)
    is_guarantor: bool = Field(False)
    physical_guarantors: List["Applicant"] = Field([])
    moral_guarantor: MoralGuarantor | None = Field(None)
    meta: Any = Field(default_factory=dict)
    documents: List[Document] = []
