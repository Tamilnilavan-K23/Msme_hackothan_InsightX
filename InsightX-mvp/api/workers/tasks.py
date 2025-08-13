from .celery_app import celery
import pandas as pd
import sqlalchemy
import os

@celery.task
def ingest_sales_task(csv_path):
    db_url = os.environ["DATABASE_URL"]
    engine = sqlalchemy.create_engine(db_url)
    df = pd.read_csv(csv_path, parse_dates=["sale_ts"])
    df.to_sql("sales", engine, if_exists="append", index=False)
    return {"rows": len(df)}
