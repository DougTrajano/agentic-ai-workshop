"""Database interface for DuckDB."""

import os
import uuid

import duckdb

from src.dataset.models.company import BusinessUnit, Department, Job
from src.dataset.models.compensation import Compensation
from src.dataset.models.employee import Employee


class Database:
    """Database interface for DuckDB.

    Provides a database abstraction layer for managing HR entities
    including employees, business units, departments, jobs, and compensation
    records. Uses DuckDB for efficient analytical queries and data processing.

    Attributes:
        file_path (str): Path to the DuckDB database file
    """

    def __init__(self, file_path: str = '../../data/hr_database.duckdb'):
        """Initialize the database connection with the specified file path.

        Args:
            file_path (str): Path to the DuckDB database file. Directory will
                           be created if it doesn't exist. Defaults to
                           "../../data/hr_database.duckdb"
        """
        self.file_path = file_path
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)

    def create_tables(self):
        """Create the complete HR database schema with all necessary tables.

        Creates tables for business_units, departments, jobs, employees, and
        compensations with proper foreign key relationships and constraints.
        This method is idempotent and safe to call multiple times.

        Tables created:
        - business_units: Top-level organizational divisions
        - departments: Functional units within business units
        - jobs: Job position definitions and classifications
        - employees: Employee personal and demographic information
        - compensations: Employee compensation packages and amounts
        """
        with duckdb.connect(self.file_path) as con:
            # Create business_units table
            con.execute("""
                CREATE TABLE IF NOT EXISTS business_units (
                    id VARCHAR PRIMARY KEY,
                    name VARCHAR NOT NULL,
                    description VARCHAR,
                    director_job_id VARCHAR NOT NULL
                );
            """)

            # Create departments table
            con.execute("""
                CREATE TABLE IF NOT EXISTS departments (
                    id VARCHAR PRIMARY KEY,
                    name VARCHAR NOT NULL,
                    description VARCHAR,
                    manager_job_id VARCHAR NOT NULL,
                    business_unit_id VARCHAR NOT NULL,
                    FOREIGN KEY (business_unit_id) REFERENCES business_units(id)
                );
            """)

            # Create jobs table
            con.execute("""
                CREATE TABLE IF NOT EXISTS jobs (
                    id VARCHAR PRIMARY KEY,
                    name VARCHAR NOT NULL,
                    description VARCHAR,
                    job_level VARCHAR NOT NULL,
                    job_family VARCHAR NOT NULL,
                    contract_type VARCHAR NOT NULL,
                    workplace_type VARCHAR NOT NULL
                );
            """)

            # Create employees table
            con.execute("""
                CREATE TABLE IF NOT EXISTS employees (
                    id VARCHAR PRIMARY KEY,
                    job_id VARCHAR NOT NULL,
                    department_id VARCHAR,
                    business_unit_id VARCHAR,
                    first_name VARCHAR NOT NULL,
                    last_name VARCHAR NOT NULL,
                    birth_date DATE NOT NULL,
                    gender VARCHAR NOT NULL,
                    ethnicity VARCHAR NOT NULL,
                    education_level VARCHAR,
                    education_field VARCHAR,
                    generation VARCHAR NOT NULL,
                    FOREIGN KEY (job_id) REFERENCES jobs(id),
                    FOREIGN KEY (department_id) REFERENCES departments(id),
                    FOREIGN KEY (business_unit_id) REFERENCES business_units(id),
                    CHECK ((department_id IS NOT NULL AND business_unit_id IS NULL) OR
                           (department_id IS NULL AND business_unit_id IS NOT NULL))
                );
            """)

            # Create compensation table
            con.execute("""
                CREATE TABLE IF NOT EXISTS compensations (
                    id VARCHAR PRIMARY KEY,
                    employee_id VARCHAR NOT NULL,
                    annual_base_salary DECIMAL(12,2) NOT NULL,
                    annual_bonus_amount DECIMAL(12,2),
                    annual_commission_amount DECIMAL(12,2),
                    rate_type VARCHAR NOT NULL,
                    total_compensation DECIMAL(12,2) NOT NULL,
                    FOREIGN KEY (employee_id) REFERENCES employees(id)
                );
            """)

    def add_employee(self, employee: Employee):
        """Insert a new employee record into the database.

        Stores complete employee information including demographics, education,
        and organizational assignments. Automatically handles UUID conversion
        and enum value extraction.

        Args:
            employee (Employee): Employee model instance containing all
                               required employee information

        Note:
            Either department_id or business_unit_id must be set, but not both,
            as enforced by the database constraint.
        """
        with duckdb.connect(self.file_path) as con:
            while True:
                try:
                    con.execute(
                        """
                        INSERT INTO employees (
                            id, job_id, department_id, business_unit_id, first_name, last_name,
                            birth_date, gender, ethnicity, education_level,
                            education_field, generation
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                        (
                            str(employee.id),
                            str(employee.job_id),
                            str(employee.department_id) if employee.department_id else None,
                            str(employee.business_unit_id) if employee.business_unit_id else None,
                            employee.first_name,
                            employee.last_name,
                            employee.birth_date,
                            employee.gender.value,
                            employee.ethnicity.value,
                            employee.education_level.value if employee.education_level else None,
                            employee.education_field.value if employee.education_field else None,
                            employee.generation.value,
                        ),
                    )
                except duckdb.ConstraintException as e:
                    print(
                        f'Failed to add employee {employee.first_name} {employee.last_name}: {e}'
                    )
                    # Regenerate UUID and retry
                    employee.id = uuid.uuid1()
                    continue
                break

    def add_business_unit(self, business_unit: BusinessUnit):
        """Insert a new business unit record into the database.

        Creates a business unit entry with its associated director job
        reference. The director job should be added separately using add_job().

        Args:
            business_unit (BusinessUnit): Business unit model instance with
                                        name, description, and director information
        """
        with duckdb.connect(self.file_path) as con:
            con.execute(
                """
                INSERT INTO business_units (id, name, description, director_job_id)
                VALUES (?, ?, ?, ?)
            """,
                (
                    str(business_unit.id),
                    business_unit.name,
                    business_unit.description,
                    str(business_unit.director.id),
                ),
            )

    def add_department(self, department: Department, business_unit_id: str):
        """Insert a new department record linked to its parent business unit.

        Creates a department entry with its manager job reference and business
        unit association. The manager job should be added separately using add_job().

        Args:
            department (Department): Department model instance with name,
                                   description, and manager information
            business_unit_id (str): UUID string of the parent business unit
        """
        with duckdb.connect(self.file_path) as con:
            con.execute(
                """
                INSERT INTO departments (id, name, description, manager_job_id, business_unit_id)
                VALUES (?, ?, ?, ?, ?)
            """,
                (
                    str(department.id),
                    department.name,
                    department.description,
                    str(department.manager.id),
                    business_unit_id,
                ),
            )

    def add_job(self, job: Job):
        """Insert a new job position record into the database.

        Stores complete job specification including level, family, contract
        type, and workplace arrangement. Automatically handles enum value
        extraction for database storage.

        Args:
            job (Job): Job model instance containing position details,
                      classifications, and work arrangements
        """
        with duckdb.connect(self.file_path) as con:
            con.execute(
                """
                INSERT INTO jobs (
                    id, name, description, job_level, job_family,
                    contract_type, workplace_type
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    str(job.id),
                    job.name,
                    job.description,
                    job.job_level.value,
                    job.job_family.value,
                    job.contract_type.value,
                    job.workplace_type.value,
                ),
            )

    def add_compensation(self, compensation: Compensation, employee_id: str):
        """Insert a compensation record linked to an employee.

        Stores complete compensation package including base salary, bonuses,
        and commissions. Automatically calculates and stores total compensation.

        Args:
            compensation (Compensation): Compensation model instance with
                                       salary and benefit information
            employee_id (str): UUID string of the associated employee
        """
        with duckdb.connect(self.file_path) as con:
            while True:
                try:
                    con.execute(
                        """
                        INSERT INTO compensations (
                            id, employee_id, annual_base_salary, annual_bonus_amount,
                            annual_commission_amount, rate_type, total_compensation
                        ) VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                        (
                            str(compensation.id),
                            employee_id,
                            compensation.annual_base_salary,
                            compensation.annual_bonus_amount,
                            compensation.annual_commission_amount,
                            compensation.rate_type.value,
                            compensation.total_compensation,
                        ),
                    )
                except duckdb.ConstraintException as e:
                    print(f'Failed to add compensation for employee {employee_id}: {e}')
                    # Regenerate UUID and retry
                    compensation.id = uuid.uuid1()
                    continue
                break
