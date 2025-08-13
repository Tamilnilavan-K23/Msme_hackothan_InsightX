from airflow import DAG
from airflow.decorators import task
from airflow.utils.dates import days_ago
from datetime import timedelta

with DAG('insightx_etl', schedule_interval='@hourly', start_date=days_ago(1), catchup=False) as dag:
    @task()
    def aggregate_hourly():
        import sqlalchemy
        engine = sqlalchemy.create_engine("postgresql://insightx:insightxpass@postgres:5432/insightx")
        q = """
        INSERT INTO metrics (metric_name, metric_ts, value, meta)
        SELECT 'sales_hourly', date_trunc('hour', sale_ts) as metric_ts, sum(total_amount) as value, jsonb_build_object('source','sales')
        FROM sales
        WHERE sale_ts > now() - interval '6 hours'
        GROUP BY 1;
        """
        with engine.begin() as conn:
            conn.execute(q)
    aggregate_hourly()
