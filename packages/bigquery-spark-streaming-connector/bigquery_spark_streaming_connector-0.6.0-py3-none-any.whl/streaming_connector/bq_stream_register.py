import stream_source.bq_stream_data_source
from stream_source.bq_stream_data_source import BQStreamDataSource
from pyspark.sql import SparkSession



spark = None
def main():
    global spark
    spark = SparkSession.builder.getOrCreate()
    spark.dataSource.register(stream_source.bq_stream_data_source.BQStreamDataSource)

if __name__ == "__main__":
    main()

