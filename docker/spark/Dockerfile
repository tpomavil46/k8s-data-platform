FROM apache/spark:4.0.0

USER root

# Versions
ENV HADOOP_VERSION=3.4.0
ENV AWS_SDK_VERSION=1.12.772
ENV DELTA_VERSION=4.0.0rc1
ENV ICEBERG_VERSION=1.7.0

# Download JARs
RUN cd /opt/spark/jars && \
    # Hadoop AWS (S3A support)
    curl -O https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/${HADOOP_VERSION}/hadoop-aws-${HADOOP_VERSION}.jar && \
    curl -O https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-bundle/${AWS_SDK_VERSION}/aws-java-sdk-bundle-${AWS_SDK_VERSION}.jar && \
    # Delta Lake
    curl -O https://repo1.maven.org/maven2/io/delta/delta-spark_2.13/${DELTA_VERSION}/delta-spark_2.13-${DELTA_VERSION}.jar && \
    curl -O https://repo1.maven.org/maven2/io/delta/delta-storage/${DELTA_VERSION}/delta-storage-${DELTA_VERSION}.jar && \
    # Iceberg
    curl -O https://repo1.maven.org/maven2/org/apache/iceberg/iceberg-spark-runtime-3.5_2.13/${ICEBERG_VERSION}/iceberg-spark-runtime-3.5_2.13-${ICEBERG_VERSION}.jar

USER 185