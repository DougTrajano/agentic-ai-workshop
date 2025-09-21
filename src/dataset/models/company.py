"""Company models for organizational structure and demographics ratios."""

from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field

from src.dataset.models.commons import BaseFields
from src.dataset.models.organizational import Job


class Industry(str, Enum):
    """Industry classifications for companies following standard industry categories.

    These classifications align with common sector groupings used in business
    and financial analysis, providing a standardized way to categorize companies
    by their primary business focus.
    """

    COMMUNICATION_SERVICES = 'Communication Services'
    CONSULTING = 'Consulting'
    CONSUMER_STAPLES = 'Consumer Staples'
    EDUCATION = 'Education'
    ENERGY = 'Energy'
    FINANCIALS = 'Financials'
    HEALTHCARE = 'Healthcare'
    INDUSTRIALS = 'Industrials'
    REAL_ESTATE = 'Real Estate'
    RETAIL = 'Retail'
    TECHNOLOGY = 'Technology'
    UTILITIES = 'Utilities'


class Department(BaseFields):
    """Specification for a department within a company's organizational structure.

    Departments represent functional units within business units, each with a
    designated manager and a specific set of job roles with defined headcounts.
    This model is used for organizational planning and synthetic data generation.
    """

    name: str = Field(..., description='Department name')
    description: Optional[str] = Field(None, description='Department description')
    manager: Job = Field(..., description='Manager of the department')
    jobs: List['JobsSpec'] = Field(
        ..., description='List of jobs and their headcount in this department'
    )

    class JobsSpec(BaseModel):
        """Specification for job distribution and headcount planning within a department.

        Defines the relationship between specific job types and their planned
        headcount allocation, enabling precise workforce planning and
        organizational structure modeling.
        """

        job: Job = Field(..., description='Job specification')
        headcount: int = Field(..., ge=1, description='Planned headcount for job')


class BusinessUnit(BaseFields):
    """Specification for a business unit within a company's organizational hierarchy.

    Business units represent major operational divisions within a company,
    each led by a director and containing multiple departments. This structure
    enables clear accountability and management hierarchy modeling.
    """

    name: str = Field(..., description='Business unit name')
    description: Optional[str] = Field(None, description='Business unit description')
    director: Job = Field(..., description='Director of the business unit')
    departments: List[Department] = Field(
        ..., description='List of departments within the business unit'
    )


class Company(BaseFields):
    """Complete specification for a company structure.

    This model guides the synthetic data generation process by defining
    the company's structure, demographics, and workforce composition.
    """

    name: str = Field(..., description='Company name')
    description: Optional[str] = Field(None, description='Company description')
    industry: Industry = Field(..., description='Industry classification')
    business_units: List[BusinessUnit] = Field(
        ..., description='List of business units within the company'
    )


class Ratios(BaseModel):
    """Demographic distribution ratios for workforce composition modeling.

    This model defines the proportional representation of different demographic
    groups within a company's workforce. All ratios should sum to 1.0 within
    each category and use 2 decimal places for precision in synthetic data generation.
    """

    gender: 'GenderRatios' = Field(..., description='Proportion of employees by gender')
    ethnicity: 'EthnicityRatios' = Field(..., description='Proportion of employees by ethnicity')
    generation: 'GenerationRatios' = Field(
        ..., description='Proportion of employees by generation'
    )

    class GenderRatios(BaseModel):
        """Proportional distribution of employees by gender identity.

        Represents the workforce composition across different gender identities,
        supporting inclusive demographic modeling. All ratios should sum to 1.0.
        """

        MALE: float = Field(..., ge=0, le=1, description='Proportion of male employees')
        FEMALE: float = Field(..., ge=0, le=1, description='Proportion of female employees')
        NON_BINARY: float = Field(
            ..., ge=0, le=1, description='Proportion of non-binary employees'
        )
        PREFER_NOT_TO_SAY: float = Field(
            ..., ge=0, le=1, description='Proportion of employees who prefer not to say'
        )

    class EthnicityRatios(BaseModel):
        """Proportional distribution of employees by ethnic background.

        Represents workforce diversity across major ethnic categories,
        enabling realistic demographic modeling. All ratios should sum to 1.0.
        """

        WHITE: float = Field(..., ge=0, le=1, description='Proportion of white employees')
        BLACK: float = Field(..., ge=0, le=1, description='Proportion of black employees')
        ASIAN: float = Field(..., ge=0, le=1, description='Proportion of Asian employees')
        HISPANIC: float = Field(..., ge=0, le=1, description='Proportion of Hispanic employees')
        OTHER: float = Field(
            ..., ge=0, le=1, description='Proportion of employees from other ethnicities'
        )

    class GenerationRatios(BaseModel):
        """Proportional distribution of employees by generational cohorts.

        Represents the age distribution of the workforce using standard
        generational categories. Enables modeling of generational diversity
        and workplace dynamics. All ratios should sum to 1.0.
        """

        BABY_BOOMER: float = Field(
            ..., ge=0, le=1, description='Proportion of Baby Boomer employees'
        )

        GEN_X: float = Field(..., ge=0, le=1, description='Proportion of Gen X employees')

        MILLENNIAL: float = Field(
            ..., ge=0, le=1, description='Proportion of Millennial employees'
        )

        GEN_Z: float = Field(..., ge=0, le=1, description='Proportion of Gen Z employees')
