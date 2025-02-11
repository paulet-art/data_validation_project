from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import pandas as pd
from pipeline import validate_data, generate_report

default_args = {
    "owner" : "Admin",
    "depends_on_past" : False,
    "retries" : 1,
    "retry_delay" : timedelta(minutes=2)
}

with DAG (
    "data_validation_dag",
    default_args = default_args,
    description = "A dag to check on data validation",
    schedule_interval = None,
    start_date = datetime(2025, 1, 1),
    catchup = False
) as dag:
    
    def load_data(**kwargs):
        file_path = "data/employee_data.csv"
        df = pd.read_csv(file_path)
        kwargs["ti"].xcom_push(key="dataframe", value=df.to_dict())

    def validate_data_task(**kwargs):
        df_dict = kwargs["ti"].xcom_pull(task_ids="load_data", key="dataframe")
        df = pd.DataFrame.from_dict(df_dict)

        validation_results = validate_data(df)

        kwargs["ti"].xcom_push(key="validation_results", value=validation_results)

    def generate_report_task(**kwargs):
        validation_results = kwargs["ti"].xcom_pull(
            task_ids="validate_data_task", key="validation_results"
        )
        report_path = "/home/paulet/Documents/data_validation_project/reports"

        generate_report(validation_results, report_path)

    load_data_task = PythonOperator(
        task_id="load_data", python_callable=load_data, provide_context=True
    )

    load_data_task >> validate_data_task >> generate_report_task

    validate_data_task = PythonOperator(
        task_id="validate_data_task", python_callable=validate_data_task, provide_contxt=True
    )

    generate_report = PythonOperator(
        task_id="generate_report_task", python_callable=generate_report, provide_context=True
    )