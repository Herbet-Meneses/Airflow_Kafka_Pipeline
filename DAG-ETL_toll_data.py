from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.utils.dates import days_ago
from datetime import timedelta

#DAG args
default_args = {
    'owner': 'HM',
    'start_date': days_ago(1),
    'email': ['fh.meneses@gmail.com'],
    'email_on_failure': True,
    'email_on_retry': True,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

#DAG definition
dag = DAG(
    dag_id= 'ETL_toll_data',
    default_args= default_args,
    description= 'Apache Airflow Final Assignment',
    schedule_interval= timedelta(days=1),
)

#Tasks
unzip_data = BashOperator(
    task_id='unzip_data',
    bash_command='tar -xvzf /home/project/airflow/dags/finalassignment/staging/tolldata.tgz -C /home/project/airflow/dags/finalassignment/staging',
    dag=dag,
)

extract_data_from_csv = BashOperator(
    task_id= 'extract_data_from_csv',
    bash_command='cut -d"," -f 1,2,3,4  /home/project/airflow/dags/finalassignment/staging/vehicle-data.csv > /home/project/airflow/dags/finalassignment/staging/csv_data.csv',
    dag=dag,
)

extract_data_from_tsv = BashOperator(
    task_id= 'extract_data_from_tsv',
    bash_command= 'cut -f 5,6,7 /home/project/airflow/dags/finalassignment/staging/tollplaza-data.tsv | sed "s/^[^\t]*/,&/" | sed "s/\t/,/g" > /home/project/airflow/dags/finalassignment/staging/tsv_data.csv',
    dag=dag,
)

extract_data_from_fixed_width = BashOperator(
    task_id= 'extract_data_from_fixed_width',
    bash_command= 'cut --characters=58-61,62-67 /home/project/airflow/dags/finalassignment/staging/payment-data.txt | sed "s/^[ \t]*//" | tr -s " " "," > /home/project/airflow/dags/finalassignment/staging/fixed_width_data.csv',
    dag=dag,
)

consolidate_data_task = BashOperator(
    task_id= 'consolidate_data',
    bash_command= 'paste /home/project/airflow/dags/finalassignment/staging/csv_data.csv /home/project/airflow/dags/finalassignment/staging/tsv_data.csv /home/project/airflow/dags/finalassignment/staging/fixed_width_data.csv > /home/project/airflow/dags/finalassignment/staging/extracted_data.csv',
    dag=dag,
)

transform_data = BashOperator(
    task_id='transform_data',
    bash_command='tr "a-z" "A-Z" < /home/project/airflow/dags/finalassignment/staging/extracted_data.csv > /home/project/airflow/dags/finalassignment/staging/transformed_data.csv',
    dag=dag,
)

#Pipeline
unzip_data >> extract_data_from_csv >> extract_data_from_tsv >> extract_data_from_fixed_width >> consolidate_data_task >> transform_data
