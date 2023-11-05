from __future__ import annotations
from airflow.operators.python import PythonOperator
from airflow.models.dag import DAG


import json
import textwrap

import pendulum

from data_ingestion.data_from_s3_bucket import data_loader_from_s3
#from Training_raw_data_validation.rawvalidation import Raw_Data_Validation
from training_Validation_insertion import train_validation
from trainingModel import trainmodel
from Model_evaluation import 
# The DAG object; we'll need this to instantiate a DAG
from airflow.models.dag import DAG

# Operators; we need this to operate!
path = "raw_data_from_s3"

from airflow.operators.python import PythonOperator
#raw_data = Raw_Data_Validation(path)
raw_validation = train_validation(path)
train = trainmodel()
# [END import_module]

# [START instantiate_dag]
with DAG(
    "sensor_training_pipeline",
    # [START default_args]
    # These args will get passed on to each operator
    # You can override them on a per-task basis during operator initialization
    default_args={"retries": 2},
    # [END default_args]
    description="DAG tutorial",
    schedule="@weekly",
    start_date=pendulum.datetime(2023, 10, 30, tz="UTC"),
    catchup=False,
    tags=["machine_learning","classification","sensor"],
) as dag:
    # [END instantiate_dag]
    # [START documentation]
    dag.doc_md = __doc__
    # [END documentation]
    
    
    def data_ingestion(**kwargs):
        ti = kwargs["ti"]
        get_data = data_loader_from_s3()
        raw_data = get_data.download_files()
        ti.xcom_push('data_ingestion',raw_data)
        
        
    def data_validation(**kwargs):
        ti = kwargs["ti"]
        valid_data = raw_validation.train_validation()
        ti.xcom_push('valid_data',valid_data)

    def model_training(**kwargs):
        ti = kwargs["ti"]
        model_trained = train.trainingmodel()
        ti.xcom_push('trained_model',model_trained)

    def model_evaluation(**kwargs):
        ti = kwargs["ti"]
        extract_file_name_schema = ti.xcom_pull(task_ids = 'values_from_schema',key = 'file_name_schema')
        LengthOfDateStampInFile,LengthOfTimeStampInFile,column_names,NumberofColumns = extract_file_name_schema

        extract_regex_schema = ti.xcom_pull(task_ids = 'regex_creation',key = 'regex_schema')
        regex = extract_regex_schema

        raw_data.raw_file_name_validation(regex,LengthOfDateStampInFile)



    values_from_schema_task = PythonOperator(
            task_id="values_from_schema",
            python_callable=values_from_schema,
        )




    regex_creation_task = PythonOperator(
            task_id="regex_creation",
            python_callable=regex_creation,
        )

    file_name_validation_task = PythonOperator(
            task_id="file_name_validation",
            python_callable=file_name_validation,
        )






    values_from_schema_task >> regex_creation_task >> file_name_validation_task


        
        
    
    
    
    
    
    
    
    
    
    
    