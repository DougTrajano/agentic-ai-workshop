"""Organizational models for job positions and contracts."""

from enum import Enum
from typing import Optional

from pydantic import Field

from src.dataset.models.commons import BaseFields


class JobLevel(str, Enum):
    """Hierarchical job level classifications for career progression tracking.

    Defines standardized levels that represent responsibility, experience,
    and authority within the organizational structure, enabling clear
    career pathing and compensation benchmarking.
    """

    INTERN = 'Intern'
    JUNIOR = 'Junior'
    MID = 'Mid'
    SENIOR = 'Senior'
    LEAD = 'Lead'
    MANAGER = 'Manager'
    DIRECTOR = 'Director'
    PRESIDENT = 'President'


class JobFamily(str, Enum):
    """Functional job family classifications grouping related roles.

    Organizes positions by functional area and skill set, facilitating
    talent management, training programs, and career development within
    similar discipline areas.
    """

    ENGINEERING = 'Engineering'
    PRODUCT = 'Product'
    DESIGN = 'Design'
    DATA = 'Data'
    MARKETING = 'Marketing'
    SALES = 'Sales'
    CUSTOMER_SUCCESS = 'Customer Success'
    FINANCE = 'Finance'
    HUMAN_RESOURCES = 'Human Resources'
    LEGAL = 'Legal'
    OPERATIONS = 'Operations'
    SECURITY = 'Security'
    QUALITY_ASSURANCE = 'Quality Assurance'
    BUSINESS_DEVELOPMENT = 'Business Development'
    EXECUTIVE = 'Executive'


class ContractType(str, Enum):
    """Employment contract classifications defining work arrangements.

    Specifies the nature of the employment relationship, affecting benefits,
    working hours, and legal obligations between employer and employee.
    """

    FULL_TIME = 'Full-Time'
    PART_TIME = 'Part-Time'
    CONTRACT = 'Contract'
    TEMPORARY = 'Temporary'
    INTERN = 'Intern'


class WorkplaceType(str, Enum):
    """Work location and arrangement classifications for modern workplace flexibility.

    Defines where and how work is performed, supporting diverse work
    arrangements and accommodating different employee preferences and
    business needs.
    """

    REMOTE = 'Remote'
    ONSITE = 'Onsite'
    HYBRID = 'Hybrid'


class Job(BaseFields):
    """Complete job position specification within the organizational structure.

    Defines a specific role with all its characteristics including level,
    functional area, contract terms, and workplace arrangements. Used for
    both organizational planning and employee assignment.
    """

    name: str = Field(..., description='Job name')
    description: Optional[str] = Field(None, description='A brief description of the job')
    job_level: JobLevel = Field(..., description='Job level classification')
    job_family: JobFamily = Field(..., description='Job family classification')
    contract_type: ContractType = Field(..., description='Contract type')
    workplace_type: WorkplaceType = Field(..., description='Type of workplace')
