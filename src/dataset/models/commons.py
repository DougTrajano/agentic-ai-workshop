"""Common fields for all models."""

import datetime
import uuid
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class BaseFields(BaseModel):
    """Base fields providing a unique identifier for all models.

    This base class ensures every model in the HR system has a consistent
    unique identifier that is automatically generated using UUID1.
    """

    id: uuid.UUID = Field(
        default_factory=uuid.uuid1, description='Auto-generated unique identifier'
    )


class StartAndEndDates(BaseModel):
    """Mixin for models that require time-bound validity periods.

    This mixin provides start and end date fields with validation to ensure
    logical date ordering. Useful for contracts, employment periods, and
    other time-limited entities.
    """

    start_date: datetime.date = Field(..., description='Start date')
    end_date: Optional[datetime.date] = Field(None, description='End date')

    @field_validator('end_date')
    @classmethod
    def validate_end_date(cls, v, values):
        """Ensure end date is after start date.

        Args:
            v: The end_date value being validated
            values: Dictionary containing other field values

        Returns:
            datetime.date: The validated end_date

        Raises:
            ValueError: If end_date is before or equal to start_date
        """
        if v and 'start_date' in values and v <= values['start_date']:
            raise ValueError('End date must be after start date')
        return v
