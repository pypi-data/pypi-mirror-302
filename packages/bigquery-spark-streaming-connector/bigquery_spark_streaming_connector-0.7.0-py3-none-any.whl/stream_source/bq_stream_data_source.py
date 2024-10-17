from pyspark.sql.datasource import DataSource
from pyspark.sql.types import StructType
from google.cloud import bigquery
from stream_source.bq_stream_reader import BQStreamReader

class BQStreamDataSource(DataSource):
    """
    An example data source for streaming data from a public API containing users' comments.
    """

    @classmethod
    def name(cls):
        return "bigquery-streaming"

    def schema(self):
        type_map = {'integer': 'long', 'float': 'double', 'record': 'string'}
        json_auth_file = "/home/" + self.options.get("service_auth_json_file_name")
        client = bigquery.Client.from_service_account_json(json_auth_file)
        table_ref = self.options.get("project_id") + '.' + self.options.get("dataset") + '.' + self.options.get("table")
        table = client.get_table(table_ref)
        original_schema = table.schema
        result = []
        for schema in original_schema:
            col_attr_name = schema.name
            if (schema.mode != 'REPEATED'):
                col_attr_type = type_map.get(schema.field_type.lower(), schema.field_type.lower())
            else:
                col_attr_type = f"array<{type_map.get(schema.field_type.lower(), schema.field_type.lower())}>"
            result.append(col_attr_name + " " + col_attr_type)

        return ",".join(result)
        # return "census_tract double,clearance_date string,clearance_status string"

    def streamReader(self, schema: StructType):
        return BQStreamReader(schema, self.options)