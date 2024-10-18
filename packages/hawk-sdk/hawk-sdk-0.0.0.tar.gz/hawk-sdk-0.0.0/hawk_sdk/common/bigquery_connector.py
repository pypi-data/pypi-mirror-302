"""
@description: Handles the connection and interaction with Google BigQuery.
@author: Rithwik Babu
"""

import os
from typing import Iterator

from google.cloud import bigquery


class BigQueryConnector:
    """Handles authentication and querying BigQuery."""

    def __init__(self, project_id: str, credentials_path: str = None) -> None:
        """Initializes BigQuery client and sets up authentication.

        :param project_id: The GCP project ID.
        :param credentials_path: Path to the Google Cloud credentials file.
        """
        if credentials_path:
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path

        if not self._validate_credentials_exists():
            raise ValueError("Credentials not found. Set GOOGLE_APPLICATION_CREDENTIALS environment variable.")

        self.client = bigquery.Client(project=project_id)

    def run_query(self, query: str) -> Iterator[bigquery.Row]:
        """Runs a SQL query on BigQuery and returns an iterator over rows.

        :param query: The SQL query to execute.
        :return: An iterator over the result rows.
        """
        query_job = self.client.query(query)
        return query_job.result()

    def _validate_credentials_exists(self) -> bool:
        """Validates if the GOOGLE_APPLICATION_CREDENTIALS environment variable is set.

        :return: True if the environment variable is set, False otherwise.
        """
        if "GOOGLE_APPLICATION_CREDENTIALS" in os.environ:
            return True
        else:
            print("Environment variable for credentials is not set.")
            return False
