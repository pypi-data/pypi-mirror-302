"""
@description: Repository layer for fetching Futures data from BigQuery.
@author: Rithwik Babu
"""

from hawk_sdk.common.bigquery_connector import BigQueryConnector
from typing import Iterator, List


class FuturesRepository:
    """Repository for accessing Futures raw data."""

    def __init__(self, connector: BigQueryConnector) -> None:
        """Initializes the repository with a BigQuery connector.

        :param connector: An instance of BigQueryConnector.
        """
        self.connector = connector

    def fetch_ohlcvo(self, start_date: str, end_date: str, interval: str, hawk_ids: List[int]) -> Iterator[dict]:
        """Fetches raw data from BigQuery for the given date range and hawk_ids.

        :param start_date: The start date for the data query (YYYY-MM-DD).
        :param end_date: The end date for the data query (YYYY-MM-DD).
        :param interval: The interval for the data query (e.g., '1d', '1h', '1m').
        :param hawk_ids: A list of specific hawk_ids to filter by.
        :return: An iterator over raw data rows.
        """
        hawk_ids_str = ', '.join(map(str, hawk_ids))
        query = f"""
        WITH records_data AS (
          SELECT 
            r.record_timestamp AS date,
            hi.value AS ticker,
            MAX(CASE WHEN f.field_name = 'open_{interval}' THEN r.double_value END) AS open,
            MAX(CASE WHEN f.field_name = 'high_{interval}' THEN r.double_value END) AS high,
            MAX(CASE WHEN f.field_name = 'low_{interval}' THEN r.double_value END) AS low,
            MAX(CASE WHEN f.field_name = 'close_{interval}' THEN r.double_value END) AS close,
            MAX(CASE WHEN f.field_name = 'volume_{interval}' THEN r.int_value END) AS volume,
            MAX(CASE WHEN f.field_name = 'open_interest_{interval}' THEN r.double_value END) AS open_interest
          FROM 
            `wsb-hc-qasap-ae2e.development.records` AS r
          JOIN 
            `wsb-hc-qasap-ae2e.development.fields` AS f
            ON r.field_id = f.field_id
          JOIN 
            `wsb-hc-qasap-ae2e.development.hawk_identifiers` AS hi
            ON r.hawk_id = hi.hawk_id
          WHERE 
            r.hawk_id IN ({hawk_ids_str})
            AND f.field_name IN ('open_1d', 'high_1d', 'low_1d', 'close_1d', 'volume_1d', 'open_interest_1d')
            AND r.record_timestamp BETWEEN '{start_date}' AND '{end_date}'
          GROUP BY 
            date, ticker
        )
        SELECT 
          date,
          ticker,
          open,
          high,
          low,
          close,
          volume,
          open_interest
        FROM 
          records_data
        ORDER BY 
          date;
        """
        return self.connector.run_query(query)
