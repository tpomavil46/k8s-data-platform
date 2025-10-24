FROM apache/spark:4.0.0

USER root

# Versions
ENV HADOOP_VERSION=3.4.0
ENV AWS_SDK_V2_VERSION=2.29.19
ENV DELTA_VERSION=4.0.0rc1
ENV ICEBERG_VERSION=1.7.0

# Download JARs
RUN cd /opt/spark/jars && \
    # Hadoop AWS (S3A support) - uses AWS SDK v2 in Hadoop 3.4.0
    curl -O https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/${HADOOP_VERSION}/hadoop-aws-${HADOOP_VERSION}.jar && \
    # AWS SDK v2 Bundle (required by Hadoop 3.4.0+)
    curl -O https://repo1.maven.org/maven2/software/amazon/awssdk/bundle/${AWS_SDK_V2_VERSION}/bundle-${AWS_SDK_V2_VERSION}.jar && \
    # Delta Lake
    curl -O https://repo1.maven.org/maven2/io/delta/delta-spark_2.13/${DELTA_VERSION}/delta-spark_2.13-${DELTA_VERSION}.jar && \
    curl -O https://repo1.maven.org/maven2/io/delta/delta-storage/${DELTA_VERSION}/delta-storage-${DELTA_VERSION}.jar && \
    # Iceberg
    curl -O https://repo1.maven.org/maven2/org/apache/iceberg/iceberg-spark-runtime-3.5_2.13/${ICEBERG_VERSION}/iceberg-spark-runtime-3.5_2.13-${ICEBERG_VERSION}.jar

USER 185
