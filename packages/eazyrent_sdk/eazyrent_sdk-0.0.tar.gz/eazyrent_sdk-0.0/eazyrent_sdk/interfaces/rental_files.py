from datetime import datetime, timezone
from typing import Any, List, Optional, Union
from uuid import UUID, uuid4

from pydantic import AwareDatetime, BaseModel, Field

from .applicants import Applicant
from .types import RENTAL_FILE_SITUATION, RENTAL_FILE_STATUS


class Tag(BaseModel):
    name: str = Field(...)


class RentalFile(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    status: RENTAL_FILE_STATUS = Field(default="NEW")
    product_id: Optional[Union[str, UUID]] = Field(
        None,
        description="The related product from product API.",
        examples=["52d7a620-f8cd-4c18-ad53-82d847d1e635"],
    )
    meta: Any = Field(
        default_factory=dict,
        examples=[
            {"reference": "FR123", "erp_id": "b5978888-829c-4630-8d94-f366be9610ec"}
        ],
    )
    applicants_situation: Optional[RENTAL_FILE_SITUATION] = Field(
        None, examples=["COUPLE"]
    )
    tags: List[Tag] = Field([])
    managers: List[str] = Field([])
    created_at: AwareDatetime | None = Field(
        default_factory=lambda: datetime.now(tz=timezone.utc)
    )
    updated_at: AwareDatetime | None = Field(None)
    score: float | None = Field(None)
    completion_rate: float | None = Field(None)
    applicants: List[Applicant]
