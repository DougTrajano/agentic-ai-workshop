# Databricks notebook source
# MAGIC %md
# MAGIC # Download HR Synthetic Dataset to Databricks Lakebase
# MAGIC
# MAGIC This notebook loads the HR Synthetic Dataset from Hugging Face and
# MAGIC populates a PostgreSQL database in Databricks Lakebase for analysis.
# MAGIC
# MAGIC **Dataset:** [dougtrajano/hr-synthetic-database](https://huggingface.co/datasets/dougtrajano/hr-synthetic-database)
# MAGIC
# MAGIC **Pipeline Steps:**
# MAGIC 1. Load dataset from Hugging Face
# MAGIC 2. Convert to Pandas DataFrames with NULL handling
# MAGIC 3. Create PostgreSQL schema and tables
# MAGIC 4. Load data respecting foreign key constraints
# MAGIC 5. Verify data integrity
# MAGIC 6. Grant permissions to Databricks App

# COMMAND ----------

# DBTITLE 1,Install Dependencies
%pip install datasets==4.1.1 pandas==2.3.3 sqlalchemy==2.0.43 psycopg[binary]==3.2.10 databricks-sdk==0.67.0

# COMMAND ----------

# DBTITLE 1,Imports and Env Vars
import os
import uuid

import pandas as pd
from datasets import load_dataset
from sqlalchemy import create_engine, text, Engine
from databricks.sdk import WorkspaceClient


os.environ['HF_DATASETS_CACHE'] = '/tmp/.cache'
os.makedirs(os.environ['HF_DATASETS_CACHE'], exist_ok=True)

# COMMAND ----------

# DBTITLE 1,Job Parameters
dbutils.widgets.text("instance_name", "", "Database Instance Name")
dbutils.widgets.text("port", "5432", "Port")
dbutils.widgets.text("database", "", "Database")
dbutils.widgets.text("schema", "human_resources", "Schema")
dbutils.widgets.text("app_name", "agentic-ai-workshop-chat-app", "App Name")
dbutils.widgets.dropdown(
    "sslmode",
    "require",
    ["disable", "allow", "prefer", "require", "verify-ca", "verify-full"],
    "SSL Mode",
)

# COMMAND ----------

# DBTITLE 1,Setup Database Connection
w = WorkspaceClient()

instance_name = dbutils.widgets.get("instance_name")
instance = w.database.get_database_instance(name=instance_name)

host = instance.read_write_dns
port = dbutils.widgets.get("port")
user = w.current_user.me().user_name
database = dbutils.widgets.get("database")
schema = dbutils.widgets.get("schema")
sslmode = dbutils.widgets.get("sslmode")

print(f"{instance_name=}")
print(f"{instance=}")
print(f"{host=}")
print(f"{port=}")
print(f"{user=}")
print(f"{database=}")
print(f"{schema=}")
print(f"{sslmode=}")

# COMMAND ----------

def create_sync_engine() -> Engine:
    """
    Create a synchronous SQLAlchemy engine for Databricks Lakebase PostgreSQL.

    Generates temporary credentials and establishes a secure connection to the
    PostgreSQL instance using SSL.

    Returns:
    Engine: SQLAlchemy engine configured for the PostgreSQL connection.
    """
    cred = w.database.generate_database_credential(
        request_id=str(uuid.uuid4()), instance_names=[instance_name]
    )

    connection_string = (
        f"postgresql://{user}:{cred.token}@{host}:{port}/"
        f"{database}?sslmode={sslmode}"
    )

    return create_engine(connection_string)

# COMMAND ----------

# DBTITLE 1,Load Dataset
business_units = load_dataset('dougtrajano/hr-synthetic-database', 'business_units')
departments = load_dataset('dougtrajano/hr-synthetic-database', 'departments')
jobs = load_dataset('dougtrajano/hr-synthetic-database', 'jobs')
employees = load_dataset('dougtrajano/hr-synthetic-database', 'employees')
compensations = load_dataset('dougtrajano/hr-synthetic-database', 'compensations')

# COMMAND ----------

# DBTITLE 1,Convert into Pandas DataFrame
import numpy as np


def clean_huggingface_nulls(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean Hugging Face dataset string representations of NULL values.

    Hugging Face datasets may contain string 'None' or empty strings instead
    of actual NULL values. This function replaces them with np.nan for proper
    NULL handling in PostgreSQL.

    Parameters:
    df (pd.DataFrame): Input DataFrame with potential string NULL values.

    Returns:
    pd.DataFrame: Cleaned DataFrame with proper NULL values.
    """
    df_clean = df.copy()
    for col in df_clean.columns:
        df_clean[col] = df_clean[col].replace(['None', ''], np.nan)
    return df_clean


# Convert Hugging Face datasets to Pandas DataFrames
df_business_units = clean_huggingface_nulls(
    pd.DataFrame(business_units['train'])
)
df_departments = clean_huggingface_nulls(
    pd.DataFrame(departments['train'])
)
df_jobs = clean_huggingface_nulls(
    pd.DataFrame(jobs['train'])
)
df_employees = clean_huggingface_nulls(
    pd.DataFrame(employees['train'])
)
df_compensations = clean_huggingface_nulls(
    pd.DataFrame(compensations['train'])
)

print(f"✅ Loaded {len(df_business_units)} business units")
print(f"✅ Loaded {len(df_departments)} departments")
print(f"✅ Loaded {len(df_jobs)} jobs")
print(f"✅ Loaded {len(df_employees)} employees")
print(f"✅ Loaded {len(df_compensations)} compensations")

# COMMAND ----------

# DBTITLE 1,Create Postgres Tables
def create_hr_tables(engine: Engine, schema_name: str) -> None:
    """
    Create HR dataset tables in PostgreSQL.

    This schema matches the Hugging Face hr-synthetic-database dataset
    structure with proper foreign key constraints and data integrity checks.

    Parameters:
    engine (Engine): SQLAlchemy engine for PostgreSQL connection.
    schema_name (str): The schema name where tables will be created.

    Raises:
    Exception: If table creation fails.
    """
    print(f"🔨 Creating HR tables in schema '{schema_name}'...")

    # Create schema
    create_schema_sql = text(f'CREATE SCHEMA IF NOT EXISTS "{schema_name}";')

    # Create all tables with proper constraints
    schema_sql = text(
        f"""
        -- Business Units Table
        CREATE TABLE IF NOT EXISTS "{schema_name}".business_units (
            id VARCHAR PRIMARY KEY,
            name VARCHAR NOT NULL,
            description VARCHAR,
            director_job_id VARCHAR NOT NULL
        );

        -- Departments Table
        CREATE TABLE IF NOT EXISTS "{schema_name}".departments (
            id VARCHAR PRIMARY KEY,
            name VARCHAR NOT NULL,
            description VARCHAR,
            manager_job_id VARCHAR NOT NULL,
            business_unit_id VARCHAR NOT NULL,
            FOREIGN KEY (business_unit_id)
                REFERENCES "{schema_name}".business_units(id)
        );

        -- Jobs Table
        CREATE TABLE IF NOT EXISTS "{schema_name}".jobs (
            id VARCHAR PRIMARY KEY,
            name VARCHAR NOT NULL,
            description VARCHAR,
            job_level VARCHAR NOT NULL,
            job_family VARCHAR NOT NULL,
            contract_type VARCHAR NOT NULL,
            workplace_type VARCHAR NOT NULL
        );

        -- Employees Table
        CREATE TABLE IF NOT EXISTS "{schema_name}".employees (
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
            FOREIGN KEY (job_id) REFERENCES "{schema_name}".jobs(id),
            FOREIGN KEY (department_id)
                REFERENCES "{schema_name}".departments(id),
            FOREIGN KEY (business_unit_id)
                REFERENCES "{schema_name}".business_units(id),
            CHECK (
                (department_id IS NOT NULL AND business_unit_id IS NULL) OR
                (department_id IS NULL AND business_unit_id IS NOT NULL)
            )
        );

        -- Compensations Table
        CREATE TABLE IF NOT EXISTS "{schema_name}".compensations (
            id VARCHAR PRIMARY KEY,
            employee_id VARCHAR NOT NULL,
            annual_base_salary DECIMAL(12,2) NOT NULL,
            annual_bonus_amount DECIMAL(12,2),
            annual_commission_amount DECIMAL(12,2),
            rate_type VARCHAR NOT NULL,
            total_compensation DECIMAL(12,2) NOT NULL,
            FOREIGN KEY (employee_id)
                REFERENCES "{schema_name}".employees(id)
        );
        """
    )

    with engine.connect() as conn:
        conn.execute(create_schema_sql)
        conn.execute(schema_sql)
        conn.commit()

    print("✅ HR tables created successfully")

# COMMAND ----------

engine = create_sync_engine()
create_hr_tables(engine, schema)

# COMMAND ----------

# DBTITLE 1,Write Data to Postgres Tables
def write_dataframes_to_postgres(
    engine: Engine, table2df: dict[str, pd.DataFrame], schema_name: str
) -> None:
    """
    Write pandas DataFrames to PostgreSQL tables.

    Respects foreign key dependencies by truncating and writing tables in the
    correct order to maintain referential integrity:
    1. jobs (no dependencies)
    2. business_units (references jobs)
    3. departments (references business_units and jobs)
    4. employees (references jobs, departments, business_units)
    5. compensations (references employees)

    Parameters:
    engine (Engine): SQLAlchemy engine for PostgreSQL connection.
    table2df (dict[str, pd.DataFrame]): Dictionary mapping table names to
        pandas DataFrames.
    schema_name (str): The schema name where tables will be written.

    Raises:
    Exception: If any table write operation fails.
    """
    print(f"📝 Writing data to schema '{schema_name}'...")

    # Define table order respecting foreign key constraints
    table_order = [
        'jobs',
        'business_units',
        'departments',
        'employees',
        'compensations'
    ]

    # Truncate tables in reverse order
    print("🗑️  Truncating existing data...")
    with engine.connect() as conn:
        for table_name in reversed(table_order):
            if table_name in table2df:
                truncate_sql = text(
                    f'TRUNCATE TABLE "{schema_name}".{table_name} CASCADE;'
                )
                conn.execute(truncate_sql)
        conn.commit()

    # Write data in correct order
    for table_name in table_order:
        if table_name in table2df:
            df = table2df[table_name]
            df.to_sql(
                name=table_name,
                con=engine,
                schema=schema_name,
                if_exists='append',
                index=False,
                method='multi',
                chunksize=1000
            )
            print(f"  ✅ {table_name}: {len(df)} rows")

    print("✅ All data written successfully")

# COMMAND ----------

table2df = {
    'jobs': df_jobs,
    'business_units': df_business_units,
    'departments': df_departments,
    'employees': df_employees,
    'compensations': df_compensations
}

write_dataframes_to_postgres(engine, table2df, schema)

# COMMAND ----------

# DBTITLE 1,Verify All Rows Are Loaded
def verify_row_counts(
    engine: Engine, table2df: dict[str, pd.DataFrame], schema_name: str
) -> None:
    """
    Verify that all rows from DataFrames were successfully loaded into tables.

    Parameters:
    engine (Engine): SQLAlchemy engine for PostgreSQL connection.
    table2df (dict[str, pd.DataFrame]): Dictionary mapping table names to
        pandas DataFrames.
    schema_name (str): The schema name where tables are located.

    Raises:
    AssertionError: If row counts don't match between DataFrame and database.
    """
    print(f"🔍 Verifying row counts in schema '{schema_name}'...")

    with engine.connect() as conn:
        for table_name, df in table2df.items():
            expected_count = len(df)
            count_query = text(
                f'SELECT COUNT(*) FROM "{schema_name}".{table_name};'
            )
            result = conn.execute(count_query)
            actual_count = result.scalar()

            assert actual_count == expected_count, (
                f"Row count mismatch for {table_name}: "
                f"expected {expected_count}, found {actual_count}"
            )
            print(f"  ✅ {table_name}: {actual_count} rows")

    print("✅ All row counts verified successfully")

# COMMAND ----------

verify_row_counts(engine, table2df, schema)

# COMMAND ----------

# DBTITLE 1,Grant Permissions to App
def grant_select_permissions(
    engine: Engine, app_id: str, schema_name: str
) -> None:
    """
    Grant SELECT permissions on all tables in the schema to a Databricks app.

    Parameters:
    engine (Engine): SQLAlchemy engine for PostgreSQL connection.
    app_id (str): The app ID to grant permissions to.
    schema_name (str): The schema name where tables are located.

    Raises:
    Exception: If permission granting fails.
    """
    print(f"🔐 Granting SELECT permissions to app '{app_id}'...")

    with engine.connect() as conn:
        # Grant schema usage
        schema_permission_sql = text(
            f'GRANT USAGE ON SCHEMA "{schema_name}" TO "{app_id}";'
        )
        conn.execute(schema_permission_sql)

        # Grant SELECT on all tables
        tables_permission_sql = text(
            f'GRANT SELECT ON ALL TABLES IN SCHEMA "{schema_name}" '
            f'TO "{app_id}";'
        )
        conn.execute(tables_permission_sql)
        conn.commit()

    print(f"✅ Granted SELECT permissions on schema '{schema_name}'")

# COMMAND ----------

app_name = dbutils.widgets.get("app_name")
app_id = w.apps.get(name=app_name).id

if app_id:
    grant_select_permissions(engine, app_id, schema)
else:
    raise ValueError(f"App with name {app_name} not found")
