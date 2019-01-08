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
    'dataflow_python_gcp_conn_id',
    schedule_interval=None,
    default_args=default_args) as dag:
    
    bash_nothing = BashOperator(task_id='nothing_2',bash_command='echo nothing')
    
    run_dataflow_python = DataFlowPythonOperator(
		    task_id='df-conn-gcp-id-from-json',
		    py_file='/home/airflow/gcs/data/wordcount.py',
		    options={'runner':'DataflowRunner',
			     'output':'gs://staging-bucket-hijo-project/out',
			     'temp_location':'gs://staging-bucket-hijo-project/teemp',
			     'staging_location':'gs://staging-bucket-hijo-project/staging',
			     'project':'hijo-project'},
		    gcp_conn_id='cloud-dataflow-hijo-project-from-location')
    bash_nothing >> run_dataflow_python
