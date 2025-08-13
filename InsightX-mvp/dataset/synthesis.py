# data/synthetic_data.py
import argparse
import random
import uuid
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

random.seed(42)
np.random.seed(42)

def gen_products(n_skus=1000):
    skus = []
    categories = ["home", "kitchen", "beauty", "sports", "electronics", "fashion"]
    for i in range(n_skus):
        sku = f"SKU-{i:04d}"
        price = round(max(1, np.random.lognormal(mean=2.5, sigma=0.8)), 2)
        lead_days = int(np.random.choice([7,14,21,30], p=[0.5,0.2,0.2,0.1]))
        skus.append({
            "sku": sku,
            "name": f"Product {i}",
            "category": random.choice(categories),
            "price": price,
            "lead_time_days": lead_days,
            "created_at": datetime.utcnow().isoformat()
        })
    return pd.DataFrame(skus)

def gen_sales(n_rows=100000, n_skus=1000, start_date="2024-01-01", days=365):
    start = datetime.fromisoformat(start_date)
    skus = [f"SKU-{i:04d}" for i in range(n_skus)]
    rows = []
    for i in range(n_rows):
        t = start + timedelta(seconds=random.randint(0, days*24*3600))
        sku = random.choice(skus)
        qty = int(np.random.poisson(1.2)) + 1
        price = round(max(0.5, np.random.lognormal(2.5, 0.8)),2)
        total = round(qty * price, 2)
        channel = random.choice(["web", "pos", "mobile"])
        rows.append({
            "sale_id": str(uuid.uuid4()),
            "sku": sku,
            "quantity": qty,
            "unit_price": price,
            "total_amount": total,
            "sale_ts": t.isoformat(),
            "channel": channel,
            "store": random.choice([f"STORE-{s:03d}" for s in range(1,21)])
        })
    return pd.DataFrame(rows)

def gen_inventory_snapshot(n_skus=1000, snap_date=None):
    if snap_date is None:
        snap_date = datetime.utcnow()
    rows = []
    for i in range(n_skus):
        sku = f"SKU-{i:04d}"
        qty_on_hand = max(0, int(np.random.normal(loc=100, scale=40)))
        reorder_point = int(max(5, qty_on_hand * np.random.uniform(0.1, 0.4)))
        rows.append({
            "snapshot_id": str(uuid.uuid4()),
            "sku": sku,
            "qty_on_hand": qty_on_hand,
            "reorder_point": reorder_point,
            "snapshot_ts": snap_date.isoformat()
        })
    return pd.DataFrame(rows)

def gen_events(n_events=20000, n_skus=1000):
    skus = [f"SKU-{i:04d}" for i in range(n_skus)]
    events = []
    start = datetime.utcnow() - timedelta(days=90)
    event_types = ["view", "add_to_cart", "purchase", "return"]
    for i in range(n_events):
        t = start + timedelta(seconds=random.randint(0, 90*24*3600))
        events.append({
            "event_id": str(uuid.uuid4()),
            "user_id": f"USER-{random.randint(1,20000):06d}",
            "sku": random.choice(skus),
            "event_type": random.choices(event_types, weights=[0.6,0.2,0.15,0.05])[0],
            "event_ts": t.isoformat()
        })
    return pd.DataFrame(events)

def main(args):
    print("Generating products...")
    df_products = gen_products(n_skus=args.skus)
    df_products.to_csv("data/products.csv", index=False)

    print("Generating sales...")
    df_sales = gen_sales(n_rows=args.rows, n_skus=args.skus, start_date=args.start, days=args.days)
    df_sales.to_csv("data/sales.csv", index=False)

    print("Generating inventory snapshot...")
    df_inv = gen_inventory_snapshot(n_skus=args.skus, snap_date=datetime.fromisoformat(args.inv_date))
    df_inv.to_csv("data/inventory.csv", index=False)

    print("Generating events...")
    df_events = gen_events(n_events=args.events, n_skus=args.skus)
    df_events.to_csv("data/events.csv", index=False)

    print("Done. Files written to data/*.csv")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--rows", type=int, default=100000)
    parser.add_argument("--skus", type=int, default=1000)
    parser.add_argument("--start", type=str, default="2024-01-01")
    parser.add_argument("--days", type=int, default=365)
    parser.add_argument("--inv_date", type=str, default=datetime.utcnow().isoformat())
    parser.add_argument("--events", type=int, default=20000)
    args = parser.parse_args()
    main(args)
