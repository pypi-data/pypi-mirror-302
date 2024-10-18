from pyspark.sql import SparkSession
from pyspark.sql.functions import max

def UniqueKey(config, *args):
    # Initialize Spark session (if not already done)
    spark = SparkSession.builder.getOrCreate()

    # Extract configuration values
    workspace_id = config["workspace_id"]
    lakehouse_id = config["lakehouse_id"]
    path = config["path"] 

    # Load the DataFrame from Delta table
    count_df = (
        spark.read
        .format("delta")
        .load(f"abfss://{workspace_id}@msit-onelake.dfs.fabric.microsoft.com/{lakehouse_id}/Tables/{path}")
        .groupBy(*args)
        .count()
    )

    # Aggregate to get the maximum value of the "count" column
    max_count_value = count_df.agg(max("count").alias("max_count")).collect()[0]["max_count"]

    # Check if max count is greater than 1
    if max_count_value > 1:
        raise Exception(f"The columns {args} are not unique in table {table}. Max count is {max_count_value}.")
    else:
        print("Unique Key validation successful.")
