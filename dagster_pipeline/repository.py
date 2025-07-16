from dagster import Definitions
from dagster_pipeline.jobs import shipping_data_pipeline
from dagster_pipeline.schedules import shipping_data_schedule

# A Dagster repository is a collection of jobs, schedules, sensors, and resources
# that Dagster can discover and run.
defs = Definitions(
    jobs=[shipping_data_pipeline],
    schedules=[shipping_data_schedule],
) 