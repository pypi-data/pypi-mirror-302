import os
from pyspark.sql.datasource import DataSourceStreamReader, InputPartition
from pyspark.sql.datasource import DataSourceStreamWriter
from pyspark.sql import Row
from pyspark.sql import SparkSession
from pyspark.sql.datasource import DataSource
from pathlib import Path
from pyarrow.lib import TimestampScalar
from datetime import datetime
from typing import Iterator, Tuple, Any, Dict, List, Sequence
from google.cloud.bigquery_storage import BigQueryReadClient, ReadSession
# from google.cloud.bigquery_storage_v1beta2.client import BigQueryReadClient
from google.cloud import bigquery_storage
import pandas
import datetime
import uuid
import time, logging

start_time = time.time()


class RangePartition(InputPartition):
    def __init__(self, session: ReadSession, stream_idx: int):
        self.session = session
        self.stream_idx = stream_idx


class BQStreamReader(DataSourceStreamReader):

    def __init__(self, schema, options):
        self.project_id = options.get("project_id")
        self.dataset = options.get("dataset")
        self.table = options.get("table")
        self.json_auth_file = "/home/"+options.get("service_auth_json_file_name")
        self.max_parallel_conn = options.get("max_parallel_conn", 1000)
        self.incremental_checkpoint_field = options.get("incremental_checkpoint_field", "")

        self.last_offset = None

    def initialOffset(self) -> dict:
        """
        Returns the initial start offset of the reader.
        """
        from datetime import datetime
        logging.info("Inside initialOffset!!!!!")
        # self.increment_latest_vals.append(datetime.strptime('1900-01-01 23:57:12', "%Y-%m-%d %H:%M:%S"))
        self.last_offset = '1900-01-01 23:57:12'

        return {"offset": str(self.last_offset)}

    def latestOffset(self):
        """
        Returns the current latest offset that the next microbatch will read to.
        """
        from datetime import datetime
        from google.cloud import bigquery

        if (self.last_offset is None):
            self.last_offset = '1900-01-01 23:57:12'

        client = bigquery.Client.from_service_account_json(self.json_auth_file)
        # max_offset=start["offset"]
        logging.info(f"************************last_offset: {self.last_offset}***********************")
        f_sql_str = ''
        for x_str in self.incremental_checkpoint_field.strip().split(","):
            f_sql_str += f"{x_str}>'{self.last_offset}' or "
        f_sql_str = f_sql_str[:-3]
        job_query = client.query(
            f"select max({self.incremental_checkpoint_field}) from {self.project_id}.{self.dataset}.{self.table} where {f_sql_str}")
        for query in job_query.result():
            max_res = query[0]

        if (str(max_res).lower() != 'none'):
            return {"offset": str(max_res)}

        return {"offset": str(self.last_offset)}

    def partitions(self, start: dict, end: dict) -> Sequence[InputPartition]:

        """
        Plans the partitioning of the current microbatch defined by start and end offset. It
        needs to return a sequence of :class:`InputPartition` objects.
        """
        if (self.last_offset is None):
            self.last_offset = end['offset']

        # if (self.last_offset==end['offset']):
        #     return []

        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = self.json_auth_file

        # project_id = self.auth_project_id

        client = BigQueryReadClient()

        # This example reads baby name data from the public datasets.
        table = "projects/{}/datasets/{}/tables/{}".format(
            self.project_id, self.dataset, self.table
        )
        requested_session = bigquery_storage.ReadSession()
        requested_session.table = table
        # requested_session.read_options.selected_fields = ["census_tract", "clearance_date", "clearance_status"]
        if (self.incremental_checkpoint_field != ''):
            start_offset = start["offset"]
            end_offset = end["offset"]
            f_sql_str = ''
            for x_str in self.incremental_checkpoint_field.strip().split(","):
                f_sql_str += f"({x_str}>'{start_offset}' and {x_str}<='{end_offset}') or "
            f_sql_str = f_sql_str[:-3]
            # requested_session.read_options.row_restriction = f"{self.incremental_checkpoint_field} > '{start_offset}' and {self.incremental_checkpoint_field} <= '{end_offset}'"
            requested_session.read_options.row_restriction = f"{f_sql_str}"

        # This example leverages Apache Avro.
        requested_session.data_format = bigquery_storage.DataFormat.AVRO

        parent = "projects/{}".format(self.project_id)
        session = client.create_read_session(
            request={
                "parent": parent,
                "read_session": requested_session,
                "max_stream_count": int(self.max_parallel_conn),
            },
        )
        self.last_offset = end['offset']
        return [RangePartition(session, i) for i in range(len(session.streams))]

    def read(self, partition) -> Iterator[List]:
        """
        Takes a partition as an input and reads an iterator of tuples from the data source.
        """
        from datetime import datetime
        session = partition.session
        stream_idx = partition.stream_idx
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = self.json_auth_file
        client_1 = BigQueryReadClient()
        # requested_session.read_options.selected_fields = ["census_tract", "clearance_date", "clearance_status"]
        reader = client_1.read_rows(session.streams[stream_idx].name)
        reader_iter = []

        for message in reader.rows():
            reader_iter_in = []
            for k, v in message.items():
                reader_iter_in.append(v)
            # yield(reader_iter)
            reader_iter.append(reader_iter_in)
            # yield (message['hash'], message['size'], message['virtual_size'], message['version'])
        # self.increment_latest_vals.append(max_incr_val)
        return iter(reader_iter)

    def commit(self, end):

        """
        This is invoked when the query has finished processing data before end offset. This
        can be used to clean up the resource.
        """
        pass