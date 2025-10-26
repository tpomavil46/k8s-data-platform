FROM ghcr.io/tpomavil46/spark-s3-delta-iceberg:4.0.1

USER root

# Install Python, pip, and JupyterLab dependencies
RUN apt-get update && apt-get install -y \
    python3-pip \
    python3-dev \
    build-essential \
    libssl-dev \
    libffi-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install JupyterLab core
RUN pip3 install --no-cache-dir \
    jupyterlab==4.0.9 \
    notebook==7.0.6 \
    jupyterhub==4.0.2

# Install data science packages
RUN pip3 install --no-cache-dir \
    pandas \
    matplotlib \
    seaborn \
    pyarrow

# Install Delta Lake and Iceberg (already have PySpark from Spark installation)
RUN pip3 install --no-cache-dir \
    delta-spark==3.2.0 \
    pyiceberg[s3fs,pyarrow]

# Create spark user for JupyterHub
RUN useradd -m -s /bin/bash -N -u 1000 jovyan && \
    mkdir -p /home/jovyan && \
    chown -R jovyan:users /home/jovyan

# Set SPARK_HOME and update PATH
ENV SPARK_HOME=/opt/spark
ENV PATH=$PATH:$SPARK_HOME/bin:$SPARK_HOME/sbin
ENV PYTHONPATH=$SPARK_HOME/python:$SPARK_HOME/python/lib/py4j-0.10.9.7-src.zip

USER jovyan
WORKDIR /home/jovyan

# Configure PySpark to find Spark
ENV PYSPARK_PYTHON=python3
ENV PYSPARK_DRIVER_PYTHON=python3

CMD ["jupyterhub-singleuser"]