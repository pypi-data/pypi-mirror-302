from pydantic import BaseModel, Field

from .types import ALERT_STATUS


class AlertType(BaseModel):
    id: str = Field(...)
    name: str = Field(...)
    description: str = Field(...)


class Alert(BaseModel):
    """Alert model."""

    alert_type: AlertType
    status: ALERT_STATUS = Field()
    comment: str | None = Field(None)
