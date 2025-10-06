"""Module for managing Databricks Lakebase credentials."""

from sqlalchemy import create_engine, event

from databricks.sdk import WorkspaceClient


workspace_client = WorkspaceClient()


def create_lakebase_engine(engine_url: str):
    """Create a SQLAlchemy engine for Lakebase with token management."""
    engine = create_engine(engine_url)

    @event.listens_for(engine, 'do_connect')
    def provide_token(dialect, conn_rec, cargs, cparams):
        """Provide the App's OAuth token. Caching is managed by WorkspaceClient."""
        cparams['password'] = workspace_client.config.oauth_token().access_token

    return engine
