from streaming_connector.bq_stream_register import *
from pyspark.sql import SparkSession
spark = SparkSession.builder.getOrCreate()
spark.dataSource.register(stream_source.bq_stream_data_source.BQStreamDataSource)