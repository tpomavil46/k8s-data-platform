FROM ghcr.io/tpomavil46/spark-s3-delta-iceberg:4.0.1

USER root

# FIRST: Remove old Spark 3.5.0
RUN rm -rf /usr/local/spark* 

# Install Python, pip, JupyterLab dependencies, and git
RUN apt-get update && apt-get install -y \
    python3-pip \
    python3-dev \
    build-essential \
    libssl-dev \
    libffi-dev \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install JupyterLab core
RUN pip3 install --no-cache-dir \
    jupyterlab==4.0.9 \
    notebook==7.0.6 \
    jupyterhub==4.0.2 \
    ipywidgets==8.1.2

# Install PySpark 4.0.1 and compatible packages
RUN pip3 install --no-cache-dir \
    pyspark==4.0.1 \
    pandas \
    matplotlib \
    seaborn \
    pyarrow \
    ipython-sql \
    sqlalchemy \
    dbt-core

RUN pip3 install --no-cache-dir \
    "sparkmagic>=0.20.5"

# Create sparkmagic config and point to Livy (adjust URL to your service)
RUN mkdir -p /etc/sparkmagic && \
    printf '%s\n' \
'{' \
'  "kernel_python_credentials": { "url": "http://livy:8998" },' \
'  "kernel_scala_credentials":  { "url": "http://livy:8998" },' \
'  "use_auto_viz": true,' \
'  "heartbeat_refresh_seconds": 3,' \
'  "heartbeat_retry_seconds": 1' \
'}' > /etc/sparkmagic/config.json

RUN chmod 644 /etc/sparkmagic/config.json

# Make Jupyter/Sparkmagic see that config by default
ENV SPARKMAGIC_CONF_DIR=/etc/sparkmagic

# Register kernels (dynamic finder)
RUN python3 - <<'PY'
import os, site, subprocess
site_pkgs = site.getsitepackages() + [site.getusersitepackages()]
sm_path = None
for base in site_pkgs:
    d = os.path.join(base, 'sparkmagic', 'kernels')
    if os.path.isdir(d):
        sm_path = d
        break
if not sm_path:
    raise SystemExit('sparkmagic kernels path not found')
for k in os.listdir(sm_path):
    kp = os.path.join(sm_path, k)
    if os.path.isdir(kp):
        subprocess.check_call(['jupyter', 'kernelspec', 'install', '--sys-prefix', kp])
print('Installed sparkmagic kernels from:', sm_path)
PY

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

# echo "# Updated $(date)" >> ~/repos/k8s-data-platform/docker/jupyter-spark/Dockerfile

# Updated Sat Nov  8 12:11:51 AM PST 2025
# Updated Sat Nov  8 10:37:11 AM PST 2025
# Updated Sun Nov  9 06:57:39 AM PST 2025
