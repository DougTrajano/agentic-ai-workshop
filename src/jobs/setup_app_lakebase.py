# Databricks notebook source
# MAGIC %md
# MAGIC # Setup Chainlit Lakebase
# MAGIC
# MAGIC This workflow sets up the Chainlit Lakebase (Databricks Managed Postgres Database), preparing necessary tables and configurations.

# COMMAND ----------

import uuid

from sqlalchemy import create_engine, text
from databricks.sdk import WorkspaceClient

# COMMAND ----------

# DBTITLE 1,Define Parameters
# Add widgets for database connection parameters
dbutils.widgets.text("instance_name", "", "Database Instance Name")
dbutils.widgets.text("port", "5432", "Port")
dbutils.widgets.text("database", "", "Database")
dbutils.widgets.text("app_name", "bi-agent", "App Name")
dbutils.widgets.dropdown(
    "sslmode",
    "require",
    ["disable", "allow", "prefer", "require", "verify-ca", "verify-full"],
    "SSL Mode",
)

# COMMAND ----------

w = WorkspaceClient()

instance_name = dbutils.widgets.get("instance_name")
instance = w.database.get_database_instance(name=instance_name)

host = instance.read_write_dns
port = dbutils.widgets.get("port")
user = w.current_user.me().user_name
database = dbutils.widgets.get("database")
sslmode = dbutils.widgets.get("sslmode")

print(f"{instance_name=}")
print(f"{instance=}")
print(f"{host=}")
print(f"{port=}")
print(f"{user=}")
print(f"{database=}")
print(f"{sslmode=}")

# COMMAND ----------

cred = w.database.generate_database_credential(
    request_id=str(uuid.uuid4()), instance_names=[instance_name]
)

connection_pool = create_engine(
    f"postgresql://{user}:{cred.token}@{host}:{port}/{database}?sslmode={sslmode}"
)

with connection_pool.connect() as conn:
    result = conn.execute(text("SELECT version()"))
    for row in result:
        print(f"Connected to PostgreSQL database. Version: {row}")

# COMMAND ----------

def create_sync_engine():
    cred = w.database.generate_database_credential(
        request_id=str(uuid.uuid4()), instance_names=[instance_name]
    )

    connection_string = (
        f"postgresql://{user}:{cred.token}@{host}:{port}/{database}?sslmode={sslmode}"
    )
    postgres_pool = create_engine(connection_string)

    return postgres_pool

# COMMAND ----------

def check_table_exists(engine, table_name: str):
    """Check if a table exists in the database"""
    query = text(
        """
    SELECT EXISTS (
        SELECT FROM information_schema.tables 
        WHERE table_schema = 'public' 
        AND table_name = :table_name
    );
    """
    )
    with engine.connect() as conn:
        result = conn.execute(query, {"table_name": table_name})
    return result.scalar()

# COMMAND ----------

def get_existing_tables(engine):
    """Get list of existing Chainlit tables"""
    query = text(
        """
    SELECT table_name
    FROM information_schema.tables 
    WHERE table_schema = 'public' 
    AND table_name IN ('users', 'threads', 'steps', 'elements', 'feedbacks', 'chat_sessions')
    ORDER BY table_name;
    """
    )
    with engine.connect() as conn:
        result = conn.execute(query)
        return [row[0] for row in result.fetchall()]

# COMMAND ----------

def setup_chainlit_schema(engine):
    """Set up the official Chainlit SQLAlchemy schema"""
    try:
        # Check existing tables
        print("🔍 Checking existing tables...")
        existing_tables = get_existing_tables(engine)

        if existing_tables:
            print(f"📋 Found existing tables: {', '.join(existing_tables)}")
            print("⚠️  Tables already exist. Skipping table creation.")
            print("✅ Schema setup complete (tables already exist)!")
            return

        print("📝 No existing tables found. Proceeding with table creation...")

        # Drop existing tables (safety measure)
        # print("🗑️ Dropping any existing tables...")
        # with engine.connect() as conn:
        #     conn.execute(text('DROP TABLE IF EXISTS feedbacks CASCADE;'))
        #     conn.execute(text('DROP TABLE IF EXISTS elements CASCADE;'))
        #     conn.execute(text('DROP TABLE IF EXISTS steps CASCADE;'))
        #     conn.execute(text('DROP TABLE IF EXISTS threads CASCADE;'))
        #     conn.execute(text('DROP TABLE IF EXISTS users CASCADE;'))
        #     conn.execute(text('DROP TABLE IF EXISTS chat_sessions CASCADE;'))
        #     conn.commit()
        # print("✅ Cleaned up any existing tables")

        # Create official Chainlit schema
        print("🔨 Creating official Chainlit schema...")
        schema_sql = text(
            """
        CREATE TABLE IF NOT EXISTS users (
            "id" UUID PRIMARY KEY,
            "identifier" TEXT NOT NULL UNIQUE,
            "metadata" JSONB NOT NULL,
            "createdAt" TEXT
        );

        CREATE TABLE IF NOT EXISTS threads (
            "id" UUID PRIMARY KEY,
            "createdAt" TEXT,
            "name" TEXT,
            "userId" UUID,
            "userIdentifier" TEXT,
            "tags" TEXT[],
            "metadata" JSONB,
            FOREIGN KEY ("userId") REFERENCES users("id") ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS steps (
            "id" UUID PRIMARY KEY,
            "name" TEXT NOT NULL,
            "type" TEXT NOT NULL,
            "threadId" UUID NOT NULL,
            "parentId" UUID,
            "streaming" BOOLEAN NOT NULL,
            "waitForAnswer" BOOLEAN,
            "isError" BOOLEAN,
            "metadata" JSONB,
            "tags" TEXT[],
            "input" TEXT,
            "output" TEXT,
            "createdAt" TEXT,
            "command" TEXT,
            "start" TEXT,
            "end" TEXT,
            "generation" JSONB,
            "showInput" TEXT,
            "language" TEXT,
            "indent" INT,
            "defaultOpen" BOOLEAN,
            FOREIGN KEY ("threadId") REFERENCES threads("id") ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS elements (
            "id" UUID PRIMARY KEY,
            "threadId" UUID,
            "type" TEXT,
            "url" TEXT,
            "chainlitKey" TEXT,
            "name" TEXT NOT NULL,
            "display" TEXT,
            "objectKey" TEXT,
            "size" TEXT,
            "page" INT,
            "language" TEXT,
            "forId" UUID,
            "mime" TEXT,
            "props" JSONB,
            FOREIGN KEY ("threadId") REFERENCES threads("id") ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS feedbacks (
            "id" UUID PRIMARY KEY,
            "forId" UUID NOT NULL,
            "threadId" UUID NOT NULL,
            "value" INT NOT NULL,
            "comment" TEXT,
            FOREIGN KEY ("threadId") REFERENCES threads("id") ON DELETE CASCADE
        );
        """
        )

        with engine.connect() as conn:
            conn.execute(schema_sql)
            conn.commit()
        print("✅ Created official Chainlit schema")

        # Verify tables were created successfully
        print("🔍 Verifying table creation...")
        created_tables = get_existing_tables(engine)

        if created_tables:
            print(f"✅ Successfully verified tables: {', '.join(created_tables)}")
        else:
            print("⚠️  Warning: No tables found after creation")

        print("✅ Schema setup complete!")

    except Exception as e:
        print(f"❌ Error setting up schema: {e}")
        import traceback

        traceback.print_exc()

# COMMAND ----------

engine = create_sync_engine()
setup_chainlit_schema(engine)

# COMMAND ----------

app_name = dbutils.widgets.get("app_name")
app_id = w.apps.get(name=app_name).id


def grant_schema_permissions(engine, app_id):
    """Grant permissions to the app"""
    try:

        schema_permission_sql = text(
            f"""
        GRANT USAGE ON SCHEMA "public" TO "{app_id}";
        """
        )

        with engine.connect() as conn:
            conn.execute(schema_permission_sql)
            conn.commit()

        print("✅ Granted schema permissions")
    except Exception as e:
        print(f"❌ Error granting schema permissions: {e}")
        import traceback

        traceback.print_exc()


def grant_table_permissions(engine, app_id):
    """Grant permissions to the app"""
    try:
        for table in ["elements", "feedbacks", "steps", "threads", "users"]:
            # Get the current user
            sql = text(
                f"""
            GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE "{database}"."public"."{table}" TO "{app_id}";
            """
            )

            with engine.connect() as conn:
                conn.execute(sql)
                conn.commit()

            print(f"✅ Granted table permissions for {table}")

    except Exception as e:
        print(f"❌ Error granting table permissions: {e}")
        import traceback


grant_schema_permissions(engine, app_id)
grant_table_permissions(engine, app_id)
