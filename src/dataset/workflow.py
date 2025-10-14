"""AI Workflow for synthetic HR data generation.

This module implements LangGraph-based AI Workflow that generates
synthetic HR data following the structured CompanySpec.
"""

import datetime
import uuid
from typing import Optional

from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.func import entrypoint, task
from pydantic import BaseModel, Field

from src.dataset.database import Database
from src.dataset.models.company import BusinessUnit, Company, Department, Ratios
from src.dataset.models.compensation import Compensation
from src.dataset.models.employee import (
    EducationField,
    EducationLevel,
    Employee,
    Ethnicity,
    Gender,
    Generation,
)
from src.dataset.models.organizational import Job
from src.dataset.utils import batch_iterator, get_birth_date, weighted_random_choice


# Tasks
@task
def get_company_spec(user_input: str) -> Company:
    """Generate a comprehensive company specification from natural language input.

    Uses OpenAI Language Model to transform user requirements into a structured Company model
    with complete organizational hierarchy including business units, departments,
    and job positions. Ensures realistic and coherent organizational structure.

    Args:
        user_input (str): Natural language description of the desired company
                         structure, industry, and characteristics

    Returns:
        Company: Structured company specification with business units,
                departments, jobs, and leadership roles properly defined

    Note:
        The LLM is instructed to create realistic organizational hierarchies
        with diverse names and common business structures.
    """
    llm = ChatOpenAI(model='gpt-4o', timeout=600, max_retries=3)

    prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessagePromptTemplate.from_template(
                'You are an experienced business strategist specializing in creating '
                'detailed organizational specifications from brief company descriptions.\n\n'
                'Your task is to design a realistic company structure that includes:\n\n'
                '- Business Units (based on product lines, regions, or functions).\n\n'
                '- Departments within each business unit (e.g., HR, IT, Sales, Marketing, Finance, etc.).\n\n'
                '- Key Roles and Jobs at different levels, ensuring diversity and realism in job titles and names.\n\n'
                'Guidelines:\n'
                '- Each business unit should be led by a Director overseeing multiple departments.\n\n'
                '- Each department should have a Manager and several distinct job roles across senior, mid-level, and junior positions.\n\n'
                '- Use realistic and varied names for all business units, departments, and roles.\n\n'
                '- Usually, a company has 3-5 business units, each with 3-7 departments, and each department with 3-10 job roles.\n\n'
                '- Ensure the organizational hierarchy is coherent and reflects common corporate structures.'
            ),
            HumanMessagePromptTemplate.from_template('{text}'),
        ]
    )

    chain = prompt | llm.with_structured_output(Company)

    response = chain.invoke({'text': user_input})
    return response


@task
def get_demographic_ratios(company_spec: Company) -> Ratios:
    """Generate realistic demographic distribution ratios for the company.

    Analyzes the company specification and industry to create appropriate
    demographic ratios that align with industry benchmarks and realistic
    workforce distributions. Uses OpenAI Language Model for intelligent ratio generation.

    Args:
        company_spec (Company): The company specification containing industry,
                               size, and organizational structure information

    Returns:
        Ratios: Demographic ratios for gender, ethnicity, and generation
               distributions that reflect realistic workforce composition

    Note:
        The LLM considers industry standards and company characteristics
        to generate statistically reasonable demographic distributions.
    """
    llm = ChatOpenAI(model='gpt-4o', timeout=60, max_retries=3)

    prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessagePromptTemplate.from_template(
                'You are an expert at defining demographic ratios '
                'based on the company specification and aligning with industry benchmarks.'
            ),
            HumanMessagePromptTemplate.from_template('{company_spec}'),
        ]
    )

    chain = prompt | llm.with_structured_output(Ratios)

    response = chain.invoke({'company_spec': company_spec.model_dump()})
    return response


@task
def get_education_fields(employee: Employee, job: Job):
    """Determine appropriate education level and field for an employee's role.

    Uses AI analysis to match employee demographics and job requirements
    with realistic education credentials. Considers job family, level,
    and industry standards to assign appropriate qualifications.

    Args:
        employee (Employee): Employee model with demographic information
        job (Job): Job model with position requirements and classifications

    Returns:
        EducationFieldsResponse: Education level and field assignments
                               that align with the job requirements
    """

    class EducationFieldsResponse(BaseModel):
        """Generates education level and field of an employee."""

        education_level: EducationLevel = Field(
            ..., description='The education level of the employee.'
        )

        education_field: EducationField = Field(
            ..., description='The field of education of the employee.'
        )

    llm = ChatOpenAI(model='gpt-5-nano', timeout=20, max_retries=5)

    prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessagePromptTemplate.from_template(
                'You are an expert HR professional who determines '
                'the education level and field of an employee based on their data and job role.'
            ),
            HumanMessagePromptTemplate.from_template(
                """{{"employee": "{employee}", "job": "{job}"}}"""
            ),
        ]
    )

    chain = prompt | llm.with_structured_output(EducationFieldsResponse)

    response: EducationFieldsResponse = chain.invoke(
        {'employee': employee.model_dump(), 'job': job.model_dump()}
    )
    return response


@task
def get_employee_compensation(employee: Employee, job: Job) -> Compensation:
    """Calculate appropriate compensation package for an employee's position.

    Analyzes employee qualifications, experience indicators, and job
    characteristics to determine realistic compensation including base
    salary, bonuses, and commissions. Considers market rates and internal equity.

    Args:
        employee (Employee): Employee model with demographics and education
        job (Job): Job model with level, family, and workplace information

    Returns:
        Compensation: Complete compensation package with base salary,
                     bonuses, and commission amounts appropriate for the role
    """
    llm = ChatOpenAI(model='gpt-5-nano', timeout=20, max_retries=5)

    prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessagePromptTemplate.from_template(
                'You are an expert HR professional who determines '
                'the compensation of an employee based on their data and job role.'
            ),
            HumanMessagePromptTemplate.from_template(
                """
                {{"employee": "{employee}", "job": "{job}"}}
                """
            ),
        ]
    )

    chain = prompt | llm.with_structured_output(Compensation)

    response = chain.invoke({'employee': employee.model_dump(), 'job': job.model_dump()})
    return response


@task
def create_database() -> None:
    """Initialize a new DuckDB database with the complete HR schema.

    Creates a fresh database instance with all necessary tables for storing
    HR data including business units, departments, jobs, employees, and
    compensation records. Sets up proper relationships and constraints.

    Returns:
        None: Database is created and initialized at the configured path

    Note:
        This operation is idempotent and safe to call multiple times.
        Uses the default database path configured in the Database class.
    """
    db = Database()
    db.create_tables()


@task
def add_department_to_db(department: Department, business_unit_id: str):
    """Add a new department record to the database."""
    db = Database()

    db.add_job(department.manager)

    for job_spec in department.jobs:
        db.add_job(job_spec.job)

    db.add_department(department, business_unit_id)


@task
def add_business_unit_to_db(business_unit: BusinessUnit):
    """Add a new business unit record to the database."""
    db = Database()
    db.add_job(business_unit.director)
    db.add_business_unit(business_unit)


@task
def add_employee_to_db(employee: Employee, compensation: Compensation):
    """Add a new employee record to the database."""
    db = Database()
    db.add_employee(employee)
    db.add_compensation(compensation, str(employee.id))


@task
def generate_employee(
    job: Job,
    birth_date: datetime.date,
    gender: Gender,
    ethnicity: Ethnicity,
    department_id: Optional[uuid.UUID] = None,
    business_unit_id: Optional[uuid.UUID] = None,
):
    """Generate employee records based on job specification and demographic ratios.

    The records will be added in the database.
    """
    employee = Employee(
        job_id=job.id,
        department_id=department_id,
        business_unit_id=business_unit_id,
        birth_date=birth_date,
        gender=gender,
        ethnicity=ethnicity,
        education_level=None,
        education_field=None,
    )

    education_fields = get_education_fields(employee, job).result()
    employee.education_level = education_fields.education_level
    employee.education_field = education_fields.education_field

    compensation = get_employee_compensation(employee, job).result()

    add_employee_to_db(employee, compensation).result()


@task
def generate_department(department: Department, ratios: Ratios):
    """Generate department records based on department specification and demographic ratios.

    The records will be added in the database.
    """
    # manager is human too
    generate_employee(
        job=department.manager,
        department_id=department.id,
        birth_date=get_birth_date(
            Generation[weighted_random_choice(ratios.generation.model_dump())]
        ),
        gender=Gender[weighted_random_choice(ratios.gender.model_dump())],
        ethnicity=Ethnicity[weighted_random_choice(ratios.ethnicity.model_dump())],
    ).result()

    for job_spec in department.jobs:
        # Parallel execution
        for batch in batch_iterator(list(range(job_spec.headcount)), batch_size=5):
            futures = [
                generate_employee(
                    job=job_spec.job,
                    department_id=department.id,
                    birth_date=get_birth_date(
                        Generation[weighted_random_choice(ratios.generation.model_dump())]
                    ),
                    gender=Gender[weighted_random_choice(ratios.gender.model_dump())],
                    ethnicity=Ethnicity[weighted_random_choice(ratios.ethnicity.model_dump())],
                )
                for _ in batch
            ]

            _ = [future.result() for future in futures]


checkpointer = InMemorySaver()


@entrypoint(checkpointer=checkpointer)
def dataset_workflow(user_input: str) -> str:
    """Complete AI-powered workflow for generating synthetic HR datasets.

    Orchestrates the end-to-end process of transforming user requirements
    into a fully populated HR database with realistic employee data.
    Combines AI-driven specification generation with systematic data creation.

    Args:
        user_input (str): Natural language description of the desired
                         company structure, industry, and characteristics

    Returns:
        str: Completion message with database information

    Workflow Steps:
        1. Generate company specification from user input
        2. Create demographic ratios based on company characteristics
        3. Initialize database with proper schema
        4. Generate business units and their directors
        5. Create departments with managers and employees
        6. Assign education and compensation to all employees

    Note:
        Uses LangGraph checkpointing for workflow state management and
        recovery. Ensures consistent demographic distributions across
        all generated employees.
    """
    company = get_company_spec(user_input).result()
    ratios = get_demographic_ratios(company).result()

    db_name = create_database().result()

    for business_unit in company.business_units:
        # Add business unit to database
        add_business_unit_to_db(business_unit).result()

        # Add director as employee
        generate_employee(
            job=business_unit.director,
            business_unit_id=business_unit.id,
            birth_date=get_birth_date(
                Generation[weighted_random_choice(ratios.generation.model_dump())]
            ),
            gender=Gender[weighted_random_choice(ratios.gender.model_dump())],
            ethnicity=Ethnicity[weighted_random_choice(ratios.ethnicity.model_dump())],
        ).result()

        # Add departments and their employees
        for department in business_unit.departments:
            add_department_to_db(department, str(business_unit.id)).result()
            generate_department(department, ratios).result()

    return f'Dataset generation completed. Database: {db_name}'
