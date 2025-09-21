"""Employee data model with detailed demographic and personal information."""

import datetime
import uuid
from enum import StrEnum
from typing import Optional

from faker import Faker
from pydantic import Field, computed_field

from src.dataset.models.commons import BaseFields


faker = Faker()


class Gender(StrEnum):
    """Gender identity classifications supporting inclusive workforce representation.

    Provides comprehensive gender categories that respect individual identity
    while enabling demographic analysis and reporting.
    """

    MALE = 'Male'
    FEMALE = 'Female'
    NON_BINARY = 'Non-binary'
    PREFER_NOT_TO_SAY = 'Prefer not to say'


class Ethnicity(StrEnum):
    """Ethnic background classifications for workforce diversity tracking.

    Enables demographic analysis and diversity reporting while respecting
    individual backgrounds and promoting inclusive workplace practices.
    """

    ASIAN = 'Asian'
    BLACK = 'Black'
    HISPANIC = 'Hispanic'
    WHITE = 'White'
    OTHER = 'Other'


class Generation(StrEnum):
    """Generational cohort classifications based on birth year ranges.

    Categorizes employees into standard generational groups for analyzing
    workplace dynamics, communication preferences, and career development needs.
    """

    BABY_BOOMER = 'Baby Boomer'
    GEN_X = 'Generation X'
    MILLENNIAL = 'Millennial'
    GEN_Z = 'Generation Z'


class EducationLevel(StrEnum):
    """Academic achievement levels for skills and qualification assessment.

    Represents the highest level of formal education completed, used for
    job matching, career development, and compensation analysis.
    """

    HIGH_SCHOOL = 'High School'
    ASSOCIATE = 'Associate Degree'
    BACHELORS = 'Bachelor Degree'
    MASTERS = 'Master Degree'
    DOCTORATE = 'Doctorate'


class EducationField(StrEnum):
    """Academic discipline classifications for specialized knowledge assessment.

    Comprehensive categorization of fields of study that enables skills
    matching, career pathing, and department alignment based on educational
    background and expertise areas.
    """

    AGRICULTURE = 'Agriculture'
    ARTS = 'Arts'
    BIOLOGICAL_SCIENCES = 'Biological Sciences'
    BUSINESS = 'Business & Management'
    COMMUNICATION_MEDIA = 'Communication, Journalism & Media'
    COMPUTER_SCIENCE = 'Computer Science'
    CIVIL_ENGINEERING = 'Civil Engineering'
    ELECTRICAL_ENGINEERING = 'Electrical Engineering'
    MECHANICAL_ENGINEERING = 'Mechanical Engineering'
    CHEMICAL_ENGINEERING = 'Chemical Engineering'
    BIOMEDICAL_ENGINEERING = 'Biomedical Engineering'
    MATERIALS_ENGINEERING = 'Materials Engineering'
    ECONOMICS = 'Economics'
    HEALTH_SCIENCES = 'Health Sciences'
    LAW = 'Law'
    LITERATURE = 'Literature'
    MATHEMATICS_STATISTICS = 'Mathematics & Statistics'
    MEDICINE = 'Medicine'
    MILITARY_SCIENCE = 'Military Science'
    NURSING = 'Nursing'
    PEDAGOGY = 'Pedagogy'
    PHARMACY = 'Pharmacy'
    PHYSICAL_SCIENCES = 'Physics & Chemistry'
    POLITICAL_SCIENCE = 'Political Science'
    PSYCHOLOGY = 'Psychology'
    RELIGIOUS_STUDIES = 'Religious Studies'
    SOCIAL_SCIENCES = 'Social Sciences'


class Employee(BaseFields):
    """Comprehensive employee record containing all personal and professional information.

    This model serves as the central employee data structure, linking together
    demographic information, educational background, and organizational placement.
    Used for both synthetic data generation and real HR system modeling.
    """

    job_id: uuid.UUID = Field(..., description='Job ID')
    department_id: Optional[uuid.UUID] = Field(None, description='Department ID')
    business_unit_id: Optional[uuid.UUID] = Field(None, description='Business Unit ID')
    birth_date: datetime.date = Field(..., description='Date of birth')
    gender: Gender = Field(..., description='Gender identification')
    ethnicity: Ethnicity = Field(..., description='Ethnicity identification')
    education_level: Optional[EducationLevel] = Field(
        None, description='Highest education level completed'
    )

    education_field: Optional[EducationField] = Field(
        None, description='Field of study for the employee'
    )

    @computed_field
    @property
    def first_name(self) -> str:
        """Generate an appropriate first name based on the employee's gender.

        Uses Faker library to generate culturally appropriate names that
        align with the employee's gender identity for realistic data modeling.

        Returns:
            str: A generated first name appropriate for the employee's gender
        """
        if self.gender == Gender.MALE:
            return faker.first_name_male()
        elif self.gender == Gender.FEMALE:
            return faker.first_name_female()
        else:
            return faker.first_name()

    @computed_field
    @property
    def last_name(self) -> str:
        """Generate an appropriate last name based on the employee's gender.

        Uses Faker library to generate culturally appropriate surnames that
        align with the employee's gender identity for consistent data modeling.

        Returns:
            str: A generated last name appropriate for the employee's gender
        """
        if self.gender == Gender.MALE:
            return faker.last_name_male()
        elif self.gender == Gender.FEMALE:
            return faker.last_name_female()
        else:
            return faker.last_name()

    @computed_field
    @property
    def generation(self) -> Generation:
        """Automatically determine generational cohort based on birth date.

        Uses standard generational date ranges to classify employees into
        appropriate cohorts for workplace analysis and management strategies.

        Returns:
            Generation: The generational category based on birth year

        Raises:
            ValueError: If birth date falls outside recognized generational ranges
        """
        if self.birth_date < datetime.date(1965, 1, 1):
            return Generation.BABY_BOOMER
        elif self.birth_date < datetime.date(1981, 1, 1):
            return Generation.GEN_X
        elif self.birth_date < datetime.date(1997, 1, 1):
            return Generation.MILLENNIAL
        elif self.birth_date < datetime.date(2016, 1, 1):
            return Generation.GEN_Z
        else:
            raise ValueError('Unknown generation')
