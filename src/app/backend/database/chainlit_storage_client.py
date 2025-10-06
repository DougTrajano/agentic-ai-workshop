"""Databricks Unity Catalog Storage Client."""

import os
from typing import Any, Dict, Optional, Union

from chainlit import make_async
from chainlit.data.storage_clients.base import BaseStorageClient
from chainlit.logger import logger


class DatabricksStorageClient(BaseStorageClient):
    """Class to enable Databricks Unity Catalog Volumes as storage provider.

        TODO: Not tested yet.

    Unity Catalog Volumes provide managed storage for files in Databricks.
    This client supports uploading, reading, and deleting files from UC Volumes.
    """

    def __init__(
        self,
        workspace_url: str,
        catalog: str,
        schema: str,
        volume: str,
        token: Optional[str] = None,
        **kwargs: Any,
    ):
        """Initialize Databricks Unity Catalog storage client.

        Args:
            workspace_url: Databricks workspace URL (e.g., 'https://my-workspace.cloud.databricks.com')
            catalog: Unity Catalog catalog name
            schema: Schema name within the catalog
            volume: Volume name within the schema
            token: Databricks personal access token (if not provided, will look for DATABRICKS_TOKEN env var)
            **kwargs: Additional configuration options
        """
        try:
            from databricks.sdk import WorkspaceClient
            from databricks.sdk.core import Config
        except ImportError:
            raise ImportError(
                'databricks-sdk is required for DatabricksStorageClient. '
                'Install it with: pip install databricks-sdk'
            )

        self.workspace_url = workspace_url.rstrip('/')
        self.catalog = catalog
        self.schema = schema
        self.volume = volume

        # Get token from parameter or environment variable
        self.token = token or os.getenv('DATABRICKS_TOKEN')
        if not self.token:
            raise ValueError(
                'Databricks token must be provided either as parameter or via DATABRICKS_TOKEN environment variable'
            )

        # Initialize Databricks workspace client
        config = Config(host=self.workspace_url, token=self.token, **kwargs)
        self.client = WorkspaceClient(config=config)

        # Construct the volume path
        self.volume_path = f'/Volumes/{catalog}/{schema}/{volume}'

        logger.info(f'DatabricksStorageClient initialized for volume: {self.volume_path}')

    def _get_full_path(self, object_key: str) -> str:
        """Construct the full path for an object in the volume."""
        # Remove leading slash if present to avoid double slashes
        object_key = object_key.lstrip('/')
        return f'{self.volume_path}/{object_key}'

    def sync_upload_file(
        self,
        object_key: str,
        data: Union[bytes, str],
        mime: str = 'application/octet-stream',
        overwrite: bool = True,
        content_disposition: str | None = None,
    ) -> Dict[str, Any]:
        """Upload a file to Databricks Unity Catalog Volume.

        Args:
            object_key: Path within the volume where the file should be stored
            data: File content as bytes or string
            mime: MIME type of the file
            overwrite: Whether to overwrite existing files
            content_disposition: Content disposition header (optional)

        Returns:
            Dict containing object_key and url
        """
        try:
            full_path = self._get_full_path(object_key)

            # Convert string data to bytes if necessary
            if isinstance(data, str):
                data = data.encode('utf-8')

            # Check if file exists and handle overwrite logic
            if not overwrite:
                try:
                    self.client.files.get_status(full_path)
                    raise Exception(f'File {object_key} already exists and overwrite is False')
                except Exception as e:
                    # If file doesn't exist, continue with upload
                    if 'does not exist' not in str(e).lower():
                        raise

            # Upload file using workspace files API
            self.client.files.upload(full_path, data, overwrite=overwrite)

            # Construct the URL for accessing the file
            url = f'{self.workspace_url}/files{full_path}'

            return {'object_key': object_key, 'url': url}

        except Exception as e:
            logger.warning(f'DatabricksStorageClient, upload_file error: {e}')
            return {}

    async def upload_file(
        self,
        object_key: str,
        data: Union[bytes, str],
        mime: str = 'application/octet-stream',
        overwrite: bool = True,
        content_disposition: str | None = None,
    ) -> Dict[str, Any]:
        """Upload a file to Databricks Unity Catalog Volume.

        Args:
            object_key: Path within the volume where the file should be stored
            data: File content as bytes or string
            mime: MIME type of the file
            overwrite: Whether to overwrite existing files
            content_disposition: Content disposition header (optional)

        Returns:
            Dict containing object_key and url
        """
        return await make_async(self.sync_upload_file)(
            object_key, data, mime, overwrite, content_disposition
        )

    def sync_delete_file(self, object_key: str) -> bool:
        """Delete a file from Databricks Unity Catalog Volume.

        Args:
            object_key: Path of the file to delete within the volume

        Returns:
            True if deletion was successful, False otherwise
        """
        try:
            full_path = self._get_full_path(object_key)
            self.client.files.delete(full_path)
            return True
        except Exception as e:
            logger.warning(f'DatabricksStorageClient, delete_file error: {e}')
            return False

    async def delete_file(self, object_key: str) -> bool:
        """Delete a file from Databricks Unity Catalog Volume.

        Args:
            object_key: Path of the file to delete within the volume

        Returns:
            True if deletion was successful, False otherwise
        """
        return await make_async(self.sync_delete_file)(object_key)

    def sync_get_read_url(self, object_key: str) -> str:
        """Get a URL for reading a file from Databricks Unity Catalog Volume.

        Note: Databricks Files API doesn't support presigned URLs like S3/GCS.
        This returns a direct URL that requires authentication.
        For public access, consider using a Databricks SQL warehouse with file serving
        or implement a proxy endpoint.

        Args:
            object_key: Path of the file within the volume

        Returns:
            URL to access the file
        """
        try:
            full_path = self._get_full_path(object_key)

            # Verify file exists
            self.client.files.get_status(full_path)

            # Return URL for accessing the file
            # Note: This URL requires authentication with Databricks
            url = f'{self.workspace_url}/files{full_path}'

            return url
        except Exception as e:
            logger.warning(f'DatabricksStorageClient, get_read_url error: {e}')
            return object_key

    async def get_read_url(self, object_key: str) -> str:
        """Get a URL for reading a file from Databricks Unity Catalog Volume.

        Note: Databricks Files API doesn't support presigned URLs like S3/GCS.
        """
        return await make_async(self.sync_get_read_url)(object_key)

    async def close(self) -> None:
        """Close the Databricks client connection."""
        # The Databricks SDK doesn't require explicit closing
        # but we'll log it for consistency
        logger.info('DatabricksStorageClient closed')
