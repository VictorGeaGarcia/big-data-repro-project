import datetime
 
from airflow import models
from airflow.contrib.operators.dataflow_operator import DataFlowPythonOperator
from airflow.operators import BashOperator
 
 
yesterday = datetime.datetime.combine(
    datetime.datetime.today() - datetime.timedelta(1),
    datetime.datetime.min.time())
 
 
default_args = {
	'start_date':yesterday
}
 
with models.DAG(
	'dataflow_bash_operator',
	schedule_interval=None,
	default_args=default_args) as dag:
        bash_command = """
        export GOOGLE_APPLICATION_CREDENTIALS=/home/airflow/gcs/data/hijo-project-sa.json
        python /home/airflow/gcs/data/wordcount.py --runner=DataflowRunner --output=gs://staging-bucket-hijo-project/out --temp_location=gs://staging-bucket-hijo-project/teemp --staging_location=gs://staging-bucket-hijo-project/staging --project=hijo-project
        """
 
	bash_nothing = BashOperator(task_id='nothing',bash_command='echo nothing')
        bash_run_job = BashOperator(task_id='run_job_from_bash_command', bash_command=bash_command)
       
        bash_nothing >> bash_run_job
