# ml/train.py
import pandas as pd
from prophet import Prophet
import joblib
import os
from datetime import datetime

def train_from_db(engine, sku, days_history=365):
    q = f"SELECT sale_ts::timestamp as ds, sum(quantity) as y FROM sales WHERE sku = '{sku}' GROUP BY 1 ORDER BY 1"
    df = pd.read_sql(q, engine, parse_dates=["ds"])
    if len(df) < 10:
        raise ValueError("not enough data")
    m = Prophet(yearly_seasonality=True, weekly_seasonality=True)
    m.fit(df)
    fname = f"ml/models/prophet_{sku}_{datetime.utcnow().strftime('%Y%m%d%H%M')}.pkl"
    os.makedirs("ml/models", exist_ok=True)
    joblib.dump(m, fname)
    return fname

if __name__ == "__main__":
    import sqlalchemy
    engine = sqlalchemy.create_engine(os.environ["DATABASE_URL"])
    # example: train top SKU
    sku = "SKU-0000"
    print(train_from_db(engine, sku))
