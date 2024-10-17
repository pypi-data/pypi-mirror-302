import datetime
from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field, ConfigDict


class Status(str, Enum):
    """
    Enum representing the status of a data request.
    """

    pending = "pending"
    acknowledged = "acknowledged"
    rejected = "rejected"
    failed = "failed"
    uploaded = "uploaded"
    completed = "completed"

    def __str__(self):
        return self.value


class BaseDataRequestModel(BaseModel):
    """
    Base model for a DataRequest.

    Attributes:
        id (UUID): Unique identifier for the data request.
        status (Status): The current status of the data request.
        composition (dict): Data composition.
        score (Optional[float]): Score associated with the data request.
        sample_label (Optional[str]): Sample label.
        analysis (Optional[dict]): Analysis data.
        expected_output (Optional[dict]): Expected output data.
        metadata (Optional[dict]): Metadata data.
    """

    status: Status
    composition: dict[str, float]
    score: Optional[float] = None
    parameters: Optional[dict] = None
    sample_label: Optional[str] = None
    analysis: Optional[list[dict]] = None
    expected_output: Optional[dict] = None
    metadata: Optional[dict] = None


class ReadDataRequest(BaseDataRequestModel):
    """
    Model for reading DataRequests.
    Used to differentiate the models if any additional fields are required for reading.
    """

    id: UUID
    created_at: datetime.datetime
    updated_at: datetime.datetime
    version: Optional[int] = 0


class CreateDataRequestModel(BaseModel):
    """
    Model for creating DataRequests.
    """

    composition: dict[str, float] = Field(..., example={"Fe": 0.5, "Ni": 0.5})
    score: Optional[float] = None
    sample_label: Optional[str] = None
    analysis: Optional[list[dict]] = Field(default=None)
    parameters: Optional[dict] = None
    expected_output: Optional[dict] = None
    metadata: Optional[dict] = None


class UpdateDataRequestModel(BaseModel):
    """
    Model for updating DataRequests.

    Attributes:
        id (UUID): Unique identifier for the data request.
        sample_label (Optional[str]): Updated sample label.
        score (Optional[float]): Updated score.
        composition (Optional[dict]): Updated composition.
    """

    id: UUID
    sample_label: Optional[str] = None
    score: Optional[float] = None
    composition: Optional[dict] = None
    parameters: Optional[dict] = None
    expected_output: Optional[dict] = None
    metadata: Optional[dict] = None


class UpdateArbitraryRequestModel(BaseModel):
    """
    Model for updating arbitrary DataRequests.

    Attributes:
        id (UUID): Unique identifier for the data request.
    """
    model_config = ConfigDict(extra="allow")

    id: UUID