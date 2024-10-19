"""For action and alerts hooks, we receive a context."""

from typing import Any

from pydantic import BaseModel

from .alerts import AlertType
from .applicants import Applicant
from .documents import Document
from .rental_files import RentalFile


class ActionContext(BaseModel):
    rental_file: Any


class DocumentAlertContext(BaseModel):
    document: Document
    applicant: Applicant
    rental_file: RentalFile
    alert_type: AlertType
