"""This module creates a data (ReAct) agent with SQL database access."""

import math
from typing import Any

import numexpr
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_community.utilities import SQLDatabase
from langchain_openai import ChatOpenAI
from langgraph.graph.state import CompiledStateGraph
from langgraph.prebuilt import create_react_agent
from pydantic import BaseModel, Field

from backend.database.lakebase import create_lakebase_engine
from backend.settings import Settings
from backend.utils import logger


class AgentOutput(BaseModel):
    """Structured output format for agent responses to user queries about data analysis.

    This model encapsulates the complete response including a natural language summary,
    the SQL query executed, the resulting dataset, and an optional visualization.
    """

    summary: str = Field(
        ...,
        description=(
            "A concise, natural language answer to the user's question that summarizes the key findings. "
            'This should directly address what the user asked and be understandable without additional context. '
            'Include specific numbers, names, or other relevant details. '
            "Example: 'The average salary across all employees is $120,000, with salaries ranging from $70,000 to $210,000.'"
        ),
    )

    sql_query: str | None = Field(
        default=None,
        description=(
            'The complete SQL query that was executed against the database to retrieve the requested data. '
            'Include this field when the answer was obtained through a database query. '
            'The query should be valid SQL that can be executed independently. '
            "Example: 'SELECT AVG(Salary) as average_salary, MIN(Salary) as min_salary, MAX(Salary) as max_salary FROM employees;'"
        ),
    )

    dataset: list[dict[str, Any]] | None = Field(
        default=None,
        description=(
            "The raw data results in Pandas DataFrame 'records' orientation format (list of dictionaries). "
            'Each dictionary represents one row, with keys as column names and values as the cell data. '
            'Include this when returning tabular data that the user can inspect or download. '
            'Limit to a reasonable number of rows (e.g., top 100) for large datasets. '
            "Example: [{'Name': 'Alice', 'Age': 25, 'Salary': 70000}, {'Name': 'Bob', 'Age': 30, 'Salary': 80000}]"
        ),
    )

    plotly_json_fig: dict | None = Field(
        default=None,
        description=(
            "A complete Plotly figure specification in JSON format that visualizes the data to answer the user's question. "
            "The JSON should contain 'data' (list of traces) and 'layout' (figure configuration) keys. "
            'Choose appropriate chart types (bar, line, scatter, pie, etc.) based on the data and question. '
            'Include meaningful titles, axis labels. This can be rendered using plotly.io.from_json(). '
            "Example: {'data': [{'type': 'bar', 'x': ['Alice', 'Bob'], 'y': [70000, 80000], 'name': 'Salary'}], "
            "'layout': {'title': 'Employee Salaries', 'xaxis': {'title': 'Name'}, 'yaxis': {'title': 'Salary ($)'}}}"
        ),
    )


def calculator(expression: str) -> str:
    """Calculate expression using Python's numexpr library.

    Expression should be a single line mathematical expression
    that solves the problem.

    Examples:
        "37593 * 67" for "37593 times 67"
        "37593**(1/5)" for "37593^(1/5)"
    """
    local_dict = {'pi': math.pi, 'e': math.e}
    return str(
        numexpr.evaluate(
            expression.strip(),
            global_dict={},  # restrict access to globals
            local_dict=local_dict,  # add common mathematical functions
        )
    )


def get_system_prompt(dialect: str, top_k: int = 5) -> str:
    """Get the system prompt for the agent."""
    system_prompt = """
    You are an agent designed to interact with a SQL database.
    Given an input question, create a syntactically correct {dialect} query to run,
    then look at the results of the query and return the answer. Unless the user
    specifies a specific number of examples they wish to obtain, always limit your
    query to at most {top_k} results.

    You can order the results by a relevant column to return the most interesting
    examples in the database. Never query for all the columns from a specific table,
    only ask for the relevant columns given the question.

    You MUST double check your query before executing it. If you get an error while
    executing a query, rewrite the query and try again.

    DO NOT make any DML statements (INSERT, UPDATE, DELETE, DROP etc.) to the
    database.

    To start you should ALWAYS look at the tables in the database to see what you
    can query. Do NOT skip this step.

    Then you should query the schema of the most relevant tables.
    """

    return system_prompt.format(
        dialect=dialect,
        top_k=top_k,
    )


def create_data_agent() -> CompiledStateGraph:
    """Create a data agent with a calculator tool and SQL database access."""
    logger.debug('Creating data agent.')

    tools = [calculator]

    llm = ChatOpenAI(model='gpt-4.1')

    # Databricks SQL Connection and tools
    logger.debug('Setting up Lakebase SQL database connection.')

    lakebase_engine = create_lakebase_engine(
        engine_url=Settings(PGDATABASE='hr_database').pg_connection_string
    )

    db = SQLDatabase(lakebase_engine)
    toolkit = SQLDatabaseToolkit(db=db, llm=llm)
    sql_tools = toolkit.get_tools()
    logger.debug('Lakebase SQL database connection established and tools created.')

    # Define the agent
    agent = create_react_agent(
        model=llm,
        tools=tools + sql_tools,
        prompt=get_system_prompt(dialect=db.dialect, top_k=5),
        response_format=AgentOutput,
    )

    logger.debug('Data agent created successfully.')
    return agent
