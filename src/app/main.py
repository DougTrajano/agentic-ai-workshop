"""Main application file for the Chainlit chat application."""

import chainlit as cl
import pandas as pd
from backend.agent import AgentOutput, create_data_agent
from backend.auth.ensure_identity import ensure_identity
from backend.database.chainlit import get_chainlit_data_layer
from backend.settings import settings
from backend.utils import logger, plotly_renderer
from chainlit.types import ThreadDict
from langchain_core.messages import HumanMessage
from langchain_core.runnables.config import RunnableConfig
from langgraph.pregel import Pregel
from starlette.datastructures import Headers


@cl.data_layer
def get_data_layer():
    """Set up the data layer for the chat application."""
    logger.info('Setting up data layer.')
    data_layer = get_chainlit_data_layer()
    return data_layer


if settings.ENABLE_HEADER_AUTH:

    @cl.header_auth_callback
    async def auth_from_header(headers: Headers) -> cl.User | None:
        """Authenticate user from headers."""
        user = headers.get('x-forwarded-preferred-username')
        token = headers.get('x-forwarded-access-token')
        email = headers.get('x-forwarded-email') or user
        if token and email:
            logger.info('[AUTH] Header auth success: %s', email)

            user = cl.User(
                identifier=email,
                display_name=user,
                metadata={
                    'auth_type': 'obo',
                    'headers': headers,
                    'email': email,
                    'provider': 'obo',
                },
            )
            return user

        logger.warning(
            '[AUTH] Header auth failed — rejecting request (no fallback in Databricks App)'
        )
        return None  # No fallback inside Databricks App

elif settings.ENABLE_PASSWORD_AUTH:
    users = {'admin': 'admin'}

    @cl.password_auth_callback
    async def auth_from_password(username: str, password: str) -> cl.User | None:
        """Authenticate user using username and password."""
        if (username, password) in users.items():
            logger.info('[AUTH] Password auth success for user: %s', username)

            user = cl.User(
                identifier=username,
                display_name=username,
                metadata={'auth_type': 'password'},
            )
            return user

        logger.warning('[AUTH] Password auth failed for user: %s', username)
        return None


@cl.set_starters
async def set_starters(user: cl.User | None = None) -> list[cl.Starter]:
    """Set the starters for the chat application."""
    return [
        cl.Starter(
            label='Female Headcount',
            message='How many female employees are in the company?',
            # icon='/public/idea.svg',
        ),
        cl.Starter(
            label='Headcount by Business Unit',
            message='Show me the headcount by business unit.',
            # icon='/public/learn.svg',
        ),
        cl.Starter(
            label='Average Salary by Job Title',
            message='What is the average salary for each job title?',
            # icon='/public/terminal.svg',
        ),
        cl.Starter(
            label='Generation Distribution',
            message='Show my headcount by generation.',
            # icon='/public/write.svg',
        ),
        cl.Starter(
            label='Generation Distribution',
            message='Show me the average salary by gender.',
            # icon='/public/write.svg',
        ),
    ]


@cl.on_chat_start
async def on_chat_start():
    """Handle the chat start event."""
    identity = await ensure_identity()
    logger.info('Identity: %s', identity)

    agent = create_data_agent()
    cl.user_session.set('agent', agent)
    logger.info('Agent initialized and stored in user session.')


@cl.on_message
async def on_message(msg: cl.Message):
    """Handle the message event."""
    identity = await ensure_identity()
    logger.info({'identity': identity, 'msg': msg.to_dict()})

    # Load the agent from the user session
    logger.debug('Retrieving agent from user session.')
    agent = cl.user_session.get('agent')
    if not isinstance(agent, Pregel):
        logger.error('Failed to retrieve a valid agent from user session.')
        await cl.Message(content='Agent not initialized.').send()
        raise ValueError('Agent not initialized.')

    config = RunnableConfig(
        configurable={'thread_id': cl.context.session.thread_id},
        recursion_limit=20,
        callbacks=[cl.LangchainCallbackHandler()],
    )

    # Data Agent
    logger.debug("Invoking agent with user's message.")
    response = agent.invoke({'messages': [HumanMessage(content=msg.content)]}, config=config)

    response = AgentOutput.model_validate(response['structured_response'])

    elements = []
    if response.plotly_json_fig:
        fig = plotly_renderer(response.plotly_json_fig)
        elements.append(cl.Plotly(name='plot', figure=fig, display='inline'))
    if response.dataset:
        df = pd.DataFrame(response.dataset)
        elements.append(cl.Dataframe(name='DataFrame', data=df, display='side'))
    await cl.Message(content=response.get_message(), elements=elements or None).send()

    # Stream the agent's response
    # final_answer = cl.Message(content='')

    # for msg, metadata in agent.stream(
    #     {'messages': [HumanMessage(content=msg.content)]}, stream_mode='messages', config=config
    # ):
    #     if (
    #         msg.content
    #         and not isinstance(msg, HumanMessage)
    #         and metadata["langgraph_node"] == "final"
    #     ):
    #         await final_answer.stream_token(msg.content)

    # await final_answer.send()


@cl.on_chat_resume
async def on_chat_resume(thread: ThreadDict):
    """Handle the chat resume event."""
    identity = await ensure_identity()
    logger.info({'identity': identity, 'thread': thread})
