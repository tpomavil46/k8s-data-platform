import duckdb
import pandas as pd

MINIO_ROOT_USER = "admin"
MINIO_ROOT_PASSWORD = "w84me@69"  # Replace with your actual password

con = duckdb.connect()

# Install and load httpfs extension
con.execute("INSTALL httpfs;")
con.execute("LOAD httpfs;")

# Configure for MinIO
con.execute("SET s3_endpoint='localhost:9000';")
con.execute(f"SET s3_access_key_id='{MINIO_ROOT_USER}';")
con.execute(f"SET s3_secret_access_key='{MINIO_ROOT_PASSWORD}';")
con.execute("SET s3_use_ssl=false;")
con.execute("SET s3_url_style='path';")

# Create sample reactor data
df = pd.DataFrame({
    'timestamp': pd.date_range('2025-10-24 08:00', periods=100, freq='1min'),
    'reactor_id': ['R-301'] * 100,
    'temperature': [145.0 + i * 0.05 for i in range(100)],
    'pressure': [8.5 + i * 0.01 for i in range(100)],
    'flow_rate': [120.0 + i * 0.1 for i in range(100)]
})

print("Sample data created:")
print(df.head())

# Write to MinIO as Parquet
con.execute("""
    COPY df TO 's3://hot-tier/demo/reactor_data.parquet'
    (FORMAT PARQUET, COMPRESSION ZSTD)
""")
print("\n✓ Wrote Parquet file to MinIO (hot-tier/demo/reactor_data.parquet)")

# Read it back and query
result = con.execute("""
    SELECT 
        COUNT(*) as row_count,
        MIN(temperature) as min_temp,
        MAX(temperature) as max_temp,
        AVG(temperature) as avg_temp,
        MIN(timestamp) as earliest,
        MAX(timestamp) as latest
    FROM read_parquet('s3://hot-tier/demo/reactor_data.parquet')
""").fetchone()

print(f"\n✓ Read back from MinIO and analyzed:")
print(f"  Rows: {result[0]}")
print(f"  Temperature: {result[1]:.2f}°C - {result[2]:.2f}°C (avg: {result[3]:.2f}°C)")
print(f"  Time Range: {result[4]} to {result[5]}")

print("\n✓ DuckDB + MinIO integration working!")
