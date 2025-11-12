FROM apache/airflow:2.10.5

USER root

# Install any system dependencies if needed
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

USER airflow

# Install dbt-postgres
RUN pip install --no-cache-dir \
    dbt-core==1.10.14 \
    dbt-postgres==1.9.1

# Copy dbt project into the image
COPY --chown=airflow:root dbt_project /opt/airflow/dbt_project

# Verify dbt installation
RUN dbt --version

USER airflow
