"""This module creates a data (ReAct) agent with SQL database access."""

import math

import numexpr
import sqlparse
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_community.utilities import SQLDatabase
from langchain_openai import ChatOpenAI
from langgraph.graph.state import CompiledStateGraph
from langgraph.prebuilt import create_react_agent
from pydantic import BaseModel, Field, field_validator

from backend.database.lakebase import create_lakebase_engine
from backend.settings import Settings
from backend.utils import logger


class AgentOutput(BaseModel):
    """Structured output format for agent responses to user queries about data analysis.

    This model encapsulates the complete response including a natural language summary,
    the SQL query executed, the resulting dataset, and an optional visualization.
    """

    content: str = Field(
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

    dataset: str | None = Field(
        default=None,
        description=(
            'A JSON-serializable representation of the dataset returned by the SQL query. '
            'This should be compatible with pandas DataFrame construction (data and columns). '
            'Include this field when the SQL query returns tabular data that supports the answer. '
            'Example: \'{"data": [[120000, 70000, 210000]], "columns": ["average_salary", "min_salary", "max_salary"]}\''
        ),
    )

    plotly_json_fig: str | None = Field(
        default=None,
        description=(
            'A Plotly JSON figure representation for visualizing the dataset. '
            'Include this field when a graphical representation of the data is helpful. '
            "IMPORTANT: Always include data labels on the chart by setting 'text' in the trace "
            "and 'textposition' to display values on the bars/points. "
            "For bar charts, use 'textposition': 'auto' or 'outside'. "
            "For scatter plots, use 'mode': 'markers+text'. "
            'Example: \'{"data": [{"type": "bar", "x": ["A", "B"], "y": [10, 20], '
            '"text": [10, 20], "textposition": "auto"}], '
            '"layout": {"title": "Sample Bar Chart"}}\''
        ),
    )

    @field_validator('sql_query')
    @classmethod
    def format_sql_query(cls, v: str | None) -> str | None:
        """Format SQL query by removing common leading whitespace."""
        if v is None:
            return None
        return sqlparse.format(v, reindent=True, keyword_case='upper', indent_width=4).strip()

    def get_message(self) -> str:
        """Get a user-friendly message summarizing the agent's response."""
        message = self.content
        if self.sql_query:
            message += f'\n\nSQL Query Executed:\n```sql\n{self.sql_query}\n```'
        return message


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

    # Define LLM
    llm = ChatOpenAI(model='gpt-4.1')

    # Define Databricks Lakebase (PostgreSQL) engine
    lakebase_engine = create_lakebase_engine(
        engine_url=Settings().pg_connection_string,
        connect_args={'options': f'-csearch_path={Settings().AGENT_SCHEMA}'},
    )

    # Define Agent tools
    tools = [calculator]
    db = SQLDatabase(lakebase_engine)
    toolkit = SQLDatabaseToolkit(db=db, llm=llm)
    sql_tools = toolkit.get_tools()

    # Define the LangGraph Agent
    agent = create_react_agent(
        model=llm,
        tools=tools + sql_tools,
        prompt=get_system_prompt(dialect=db.dialect, top_k=5),
        response_format=AgentOutput,
    )

    logger.debug('Data agent created successfully.')
    return agent
