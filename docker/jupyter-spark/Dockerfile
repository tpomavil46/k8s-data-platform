FROM ghcr.io/tpomavil46/spark-s3-delta-iceberg:4.0.1

USER root

# FIRST: Remove old Spark 3.5.0
RUN rm -rf /usr/local/spark* 

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

# Install PySpark 4.0.1 and compatible packages
RUN pip3 install --no-cache-dir \
    pyspark==4.0.1 \
    pandas \
    matplotlib \
    seaborn \
    pyarrow

# Install Delta Lake for Spark 4.0
RUN pip3 install --no-cache-dir \
    delta-spark==4.0.0 \
    pyiceberg[s3fs,pyarrow]

# Create spark user for JupyterHub
RUN useradd -m -s /bin/bash -N -u 1000 jovyan && \
    mkdir -p /home/jovyan && \
    chown -R jovyan:users /home/jovyan

USER jovyan
WORKDIR /home/jovyan

# Set environment variables
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV PYSPARK_PYTHON=python3
ENV PYSPARK_DRIVER_PYTHON=python3

CMD ["jupyterhub-singleuser"]