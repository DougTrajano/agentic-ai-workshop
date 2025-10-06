"""Utility functions for the chat application."""

import json
import logging

import plotly.graph_objects as go
import plotly.io as pio

from backend.settings import settings


class JSONFormatter(logging.Formatter):
    """Custom JSON formatter for structured logging."""

    def format(self, record: logging.LogRecord) -> str:
        """Format the log record as a JSON string.

        Args:
            record (logging.LogRecord): The log record to format.

        Returns:
            str: A JSON-formatted log entry.
        """
        log_data = {
            'timestamp': self.formatTime(record, self.datefmt),
            # "name": record.name,
            'level': record.levelname,
            'pathname': record.pathname,
            'lineno': record.lineno,
            'funcName': record.funcName,
            'message': record.getMessage(),
        }

        # Add exception info if present
        if record.exc_info:
            log_data['exc_info'] = self.formatException(record.exc_info)

        # Add stack info if present
        if hasattr(record, 'stack_info') and record.stack_info:
            log_data['stack_info'] = self.formatStack(record.stack_info)

        return json.dumps(log_data, ensure_ascii=False)


# Configure logger with JSON formatter
handler = logging.StreamHandler()
handler.setFormatter(JSONFormatter(datefmt='%Y-%m-%d %H:%M:%S'))

logger = logging.getLogger(__name__)
logger.setLevel(settings.LOG_LEVEL)
logger.addHandler(handler)
logger.propagate = False


def plotly_renderer(json_fig: dict) -> go.Figure | go.FigureWidget:
    """Render a Plotly figure from its JSON representation and update its theme to 'plotly_dark'.

    Args:
        json_fig (dict): The JSON representation of the Plotly figure.

    Returns:
        go.Figure | go.FigureWidget: The rendered Plotly figure.
    """
    fig = pio.from_json(json_fig, skip_invalid=True)

    # Update theme to 'plotly_dark'
    fig.update_layout(template='plotly_dark')
    return fig
