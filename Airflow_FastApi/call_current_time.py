from airflow import DAG
from datetime import datetime
from airflow.operators.python import PythonOperator
import pandas as pd
import requests

# Define the DAG for extracting, transforming, and loading current time data
with DAG(
    dag_id="current_time",  # DAG identifier
    start_date=datetime(year=2024, month=12, day=21, hour=9, minute=0),  # DAG start date and time
    schedule="@hourly",  # Schedule to run every hour
    catchup=False,  # Do not backfill missing runs
    max_active_runs=1,  # Allow only one active DAG run at a time
    render_template_as_native_obj=True  # Enable native object rendering in templates
) as dag:

    # Define the function to extract data from the API
    def extract_data_callable():
        """
        Extract the current time from a local API endpoint.
        """
        print("Extracting current time from API")  # Log a message
        url = "http://127.0.0.1:8000/time/"  # API endpoint

        # Make a GET request to the API and parse the response
        date_obj = requests.get(url).json()

        # Create a dictionary to store the extracted date
        date_dic = {"date": date_obj}

        return date_dic  # Return the extracted data

    # Define the PythonOperator for extracting data
    extract_data = PythonOperator(
        dag=dag,
        task_id="extract_time",  # Task identifier
        python_callable=extract_data_callable  # Function to execute
    )

    # Define the function to transform the extracted data
    def transform_data_callable(raw_data):
        """
        Transform the extracted data into a list format.
        """
        transformed_data = [
            [
                raw_data.get("date"),  # Extract the "date" field
            ]
        ]
        return transformed_data  # Return the transformed data

    # Define the PythonOperator for transforming data
    transform_data = PythonOperator(
        dag=dag,
        task_id="transform_data",  # Task identifier
        python_callable=transform_data_callable,  # Function to execute
        op_kwargs={"raw_data": "{{ ti.xcom_pull(task_ids='extract_time') }}"}  # Pass data from the previous task
    )

    # Define the function to load the transformed data
    def load_data_callable(transformed_data):
        """
        Load the transformed data into a pandas DataFrame and print it.
        """
        # Create a DataFrame from the transformed data
        loaded_data = pd.DataFrame(transformed_data)

        # Set column names for the DataFrame
        loaded_data.columns = [
            "date"
        ]
        
        # Print the DataFrame
        print(loaded_data)

    # Define the PythonOperator for loading data
    load_data = PythonOperator(
        dag=dag,
        task_id="load_data",  # Task identifier
        python_callable=load_data_callable,  # Function to execute
        op_kwargs={"transformed_data": "{{ ti.xcom_pull(task_ids='transform_data') }}"}  # Pass data from the previous task
    )

    # Set dependencies between tasks
    extract_data >> transform_data >> load_data  # Define the task sequence