"""Database setup for Chainlit integration."""

from chainlit.data.sql_alchemy import SQLAlchemyDataLayer
from sqlalchemy import event

from backend.settings import settings
from databricks.sdk import WorkspaceClient


workspace_client = WorkspaceClient()


def get_chainlit_data_layer() -> SQLAlchemyDataLayer:
    """Set up the data layer for the chat application."""
    data_layer = SQLAlchemyDataLayer(settings.pg_connection_string)

    engine = data_layer.engine
    # For async engines, we need to use the sync engine for event listeners
    if hasattr(engine, 'sync_engine'):
        sync_engine = engine.sync_engine
    else:
        sync_engine = engine

    @event.listens_for(sync_engine, 'do_connect')
    def provide_token(dialect, conn_rec, cargs, cparams):
        cparams['password'] = workspace_client.config.oauth_token().access_token

    return data_layer
