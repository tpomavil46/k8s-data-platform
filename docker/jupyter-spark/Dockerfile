FROM ghcr.io/tpomavil46/spark-s3-delta-iceberg:4.0.1

USER root

# Remove old Spark 3.5.0
RUN rm -rf /usr/local/spark*

# System deps (added nano)
RUN apt-get update && apt-get install -y \
    python3-pip python3-dev build-essential \
    libssl-dev libffi-dev curl git nano \
    && rm -rf /var/lib/apt/lists/*

# Make pip behave well on system Python
ENV PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_BREAK_SYSTEM_PACKAGES=1

# Upgrade pip toolchain early
RUN python3 -m pip install -U pip setuptools wheel

# === Classic Jupyter stack that sparkmagic works with ===
RUN pip3 install \
    jupyterlab==3.6.7 \
    notebook==6.5.7 \
    jupyterhub==4.0.2 \
    ipywidgets==8.1.2 \
    'jupyter-ai[all]'

# Core Python libs
RUN pip3 install \
    pyspark==4.0.1 \
    pandas matplotlib seaborn pyarrow \
    ipython-sql sqlalchemy dbt-core

# Kerberos headers needed to build gssapi (requested via pyspnego[kerberos])
RUN apt-get update && apt-get install -y \
    libkrb5-dev pkg-config \
 && rm -rf /var/lib/apt/lists/*

# Sparkmagic (known-good with classic stack)
RUN pip3 install sparkmagic==0.20.5

# Sparkmagic config (points to your Livy)
RUN mkdir -p /etc/sparkmagic && cat > /etc/sparkmagic/config.json <<'JSON'
{
  "kernel_python_credentials": { "url": "http://livy:8998" },
  "kernel_scala_credentials":  { "url": "http://livy:8998" },
  "use_auto_viz": true,
  "heartbeat_refresh_seconds": 3,
  "heartbeat_retry_seconds": 1
}
JSON
RUN chmod 644 /etc/sparkmagic/config.json
ENV SPARKMAGIC_CONF_DIR=/etc/sparkmagic

# Register sparkmagic kernels
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

# Delta + Iceberg
RUN pip3 install delta-spark==4.0.0 "pyiceberg[s3fs,pyarrow]"

# Create user
RUN useradd -m -s /bin/bash -N -u 1000 jovyan && \
    mkdir -p /home/jovyan && chown -R jovyan:users /home/jovyan

USER jovyan
WORKDIR /home/jovyan

# Env
ENV SHELL=/bin/bash
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV PYSPARK_PYTHON=python3
ENV PYSPARK_DRIVER_PYTHON=python3

CMD ["jupyterhub-singleuser"]

