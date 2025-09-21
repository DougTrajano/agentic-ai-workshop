"""Compensation package models for HR system."""

from enum import Enum

from pydantic import Field

from src.dataset.models.commons import BaseFields


class RateType(str, Enum):
    """Classification of compensation payment structures.

    Defines whether an employee is paid on an hourly basis or receives
    a fixed annual salary, affecting how compensation is calculated
    and administered.
    """

    HOURLY = 'Hourly'
    SALARY = 'Salary'


class Compensation(BaseFields):
    """The compensation package information for an employee."""

    annual_base_salary: float = Field(..., ge=1, description='Base annual salary')
    annual_bonus_amount: float | None = Field(None, ge=0, description='Annual bonus amount')
    annual_commission_amount: float | None = Field(
        None, ge=0, description='Annual commission amount (usually a percentage of sales)'
    )

    rate_type: RateType = Field(..., description='Type of compensation rate')

    @property
    def total_compensation(self) -> float:
        """Calculate the total annual compensation including all components.

        Returns:
            float: Sum of base salary, bonus amount, and commission amount.
                   None values are treated as zero in the calculation.
        """
        return (
            self.annual_base_salary
            + (self.annual_bonus_amount or 0)
            + (self.annual_commission_amount or 0)
        )
