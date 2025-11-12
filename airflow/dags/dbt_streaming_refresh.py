run_dbt = BashOperator(
    task_id='run_dbt_models',
    bash_command='''
        cd /opt/airflow/dbt_project && \
        dbt run
    ''',
    env={
        'POSTGRES_HOST': '172.16.0.20',
        'POSTGRES_DB': 'myapp',
        'POSTGRES_USER': 'streamuser',
        'POSTGRES_PASSWORD': 'w84me@69',  # Or use Airflow connection
    },
    dag=dag,
)