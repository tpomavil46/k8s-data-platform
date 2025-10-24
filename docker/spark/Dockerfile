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
    # Delta Lake (check for Spark 4.0 compatibility)
    curl -O https://repo1.maven.org/maven2/io/delta/delta-spark_2.13/${DELTA_VERSION}/delta-spark_2.13-${DELTA_VERSION}.jar && \
    curl -O https://repo1.maven.org/maven2/io/delta/delta-storage/${DELTA_VERSION}/delta-storage-${DELTA_VERSION}.jar && \
    # Iceberg
    curl -O https://repo1.maven.org/maven2/org/apache/iceberg/iceberg-spark-runtime-3.5_2.13/${ICEBERG_VERSION}/iceberg-spark-runtime-3.5_2.13-${ICEBERG_VERSION}.jar

# Add default Spark configurations for Delta and Iceberg (as root, before switching users)
RUN echo "spark.sql.extensions=io.delta.sql.DeltaSparkSessionExtension,org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions" >> /opt/spark/conf/spark-defaults.conf && \
    echo "spark.sql.catalog.spark_catalog=org.apache.spark.sql.delta.catalog.DeltaCatalog" >> /opt/spark/conf/spark-defaults.conf && \
    echo "spark.sql.catalog.iceberg=org.apache.iceberg.spark.SparkCatalog" >> /opt/spark/conf/spark-defaults.conf && \
    echo "spark.sql.catalog.iceberg.type=hadoop" >> /opt/spark/conf/spark-defaults.conf && \
    echo "spark.sql.catalog.iceberg.warehouse=s3a://data/warehouse" >> /opt/spark/conf/spark-defaults.conf && \
    chown -R 185:185 /opt/spark/conf

USER 185