from __future__ import annotations
from airflow.operators.python import PythonOperator
from airflow.models.dag import DAG


import json
import textwrap

import pendulum

#from data_ingestion.data_from_s3_bucket import data_loader_from_s3
#from Training_raw_data_validation.rawvalidation import Raw_Data_Validation
#from training_Validation_insertion import train_validation


# The DAG object; we'll need this to instantiate a DAG
from airflow.models.dag import DAG

# Operators; we need this to operate!
#path = "raw_data_from_s3"

from airflow.operators.python import PythonOperator
#raw_data = Raw_Data_Validation(path)



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
        from data_ingestion.data_from_s3_bucket import data_loader_from_s3
        get_data = data_loader_from_s3('waferbucket')
        raw_data_path = get_data.download_files()
        ti.xcom_push('raw_data',raw_data_path)
        
        
    def data_validation(**kwargs):
        ti = kwargs["ti"]
        from training_Validation_insertion import train_validation
        raw_data_path = ti.xcom_pull(task_ids = 'data_ingestion',key = 'raw_data')
        raw_validation = train_validation(raw_data_path)
        valid_data = raw_validation.train_validation()
        ti.xcom_push('valid_data',valid_data)

    def model_training(**kwargs):
        ti = kwargs["ti"]
        from trainingModel import trainmodel
        train = trainmodel()
        model_trained = train.trainingmodel()
        ti.xcom_push('trained_model',model_trained)
        

    def model_evaluation(**kwargs):
        ti = kwargs["ti"]
        from Model_evaluation import evaluate_model
        model_eval = evaluate_model()
        model_eval.model_prediction()
        eval_model = model_eval.calculate_metrics_score()
        ti.xcom_push("evaluate_model",eval_model)
        

        

    data_ingestion_task = PythonOperator(
            task_id="data_ingestion",
            python_callable=data_ingestion,
        )


    data_validation_task = PythonOperator(
            task_id="data_validation",
            python_callable=data_validation,
        )

    model_training_task = PythonOperator(
            task_id="model_training",
            python_callable=model_training,
        )
    
    model_evaluation_task = PythonOperator(
            task_id="model_evaluation",
            python_callable=model_evaluation,
        )





    data_ingestion_task >> data_validation_task >> model_training_task >> model_evaluation_task


        
        
    
    
    
    
    
    
    
    
    
    
    