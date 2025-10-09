"""Ensure user identity is available."""

from typing import Dict

import chainlit as cl

from backend.auth.identity import Identity, OboTokenSource, PatTokenSource
from backend.settings import settings
from backend.utils import logger


async def ensure_identity():
    """Ensure the user identity is available and return it.

    Note: When running in Databricks Apps, the runtime manages token lifecycle
    and provides fresh tokens in headers on every request. We don't need to
    validate token expiration as Databricks handles this automatically.
    """
    if not cl.context.session:
        logger.error('[AUTH] No session context available')
        return None

    user = cl.context.session.user
    if not user:
        logger.warning('[AUTH] User not found for this session. Please login again.')
        return None

    # For PAT auth, it's simple - just use the configured PAT
    if settings.ENABLE_PASSWORD_AUTH and settings.DATABRICKS_TOKEN:
        logger.info('[AUTH] Using PAT authentication')
        return Identity(
            email=user.identifier,
            display_name=user.display_name,
            auth_type='pat',
            token_source=PatTokenSource(settings.DATABRICKS_TOKEN),
        )

    # For OBO auth, we need to get headers from user metadata
    # Databricks Apps refreshes these headers on every request
    auth_type = 'obo'
    token_source = None

    # Get stored headers from user metadata
    if user.metadata:
        stored_headers = user.metadata.get('headers')

        if stored_headers:
            # Use stored headers - Databricks Apps keeps these fresh
            def _stored_headers_getter() -> Dict[str, str]:
                return stored_headers

            token_source = OboTokenSource(_stored_headers_getter)
            logger.info('[AUTH] Using OBO authentication with Databricks-managed token')
        else:
            logger.warning('[AUTH] No stored headers found in user metadata')

    # If no stored headers available, we can't proceed
    if not token_source:
        logger.error('[AUTH] No OBO headers available - user needs to re-authenticate')
        return None

    # Validate we have a token (but don't check expiration - Databricks manages that)
    token = token_source.bearer_token()
    if not token:
        logger.error('[AUTH] No OBO token found in headers')
        return None

    logger.info('[AUTH] Valid authentication ready')
    return Identity(
        email=getattr(user, 'email', None),
        display_name=user.display_name,
        auth_type=auth_type,
        token_source=token_source,
    )
