from dagster import ScheduleDefinition
from dagster_pipeline.jobs import shipping_data_pipeline

shipping_data_schedule = ScheduleDefinition(
    job=shipping_data_pipeline,
    cron_schedule="0 2 * * *",  # Every day at 2am
    execution_timezone="UTC"
)
"""
This schedule runs the shipping_data_pipeline job every day at 2am UTC.
""" 