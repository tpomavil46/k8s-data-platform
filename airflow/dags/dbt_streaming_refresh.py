from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.pod import KubernetesPodOperator
from kubernetes.client import models as k8s
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2025, 11, 12),
    'retries': 1,
    'retry_delay': timedelta(seconds=30),
}

dag = DAG(
    'dbt_streaming_refresh',
    default_args=default_args,
    description='Run dbt every 2 minutes via KubernetesPodOperator',
    schedule_interval='*/2 * * * *',
    catchup=False,
    tags=['dbt', 'streaming'],
)

run_dbt = KubernetesPodOperator(
    task_id='run_dbt_models',
    name='dbt-streaming-run',
    namespace='streaming-demo',
    image='ghcr.io/tpomavil46/k8s-data-platform/dbt-streaming-demo:latest',
    cmds=['dbt', 'run'],
    env_from=[
        k8s.V1EnvFromSource(
            secret_ref=k8s.V1SecretEnvSource(name='dbt-env')
        )
    ],
    get_logs=True,
    is_delete_operator_pod=True,
    in_cluster=True,
    dag=dag,
)