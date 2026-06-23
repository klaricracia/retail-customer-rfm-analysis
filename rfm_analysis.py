"""
RFM Customer Segmentation Analysis
====================================
Author: Klarissa Artavia — Data & AI Strategy
GitHub: https://github.com/klaricracia
LinkedIn: https://www.linkedin.com/in/klariartavia/

What this script does:
  1. Loads retail transaction data
  2. Calculates RFM (Recency, Frequency, Monetary) scores per customer
  3. Segments customers into actionable loyalty tiers
  4. Exports results to /output for dashboard consumption

Dataset: UCI Online Retail (or any CSV with CustomerID, InvoiceDate, InvoiceNo, TotalAmount)
"""

import pandas as pd
import numpy as np
from datetime import datetime
import os

# ── Configuration ──────────────────────────────────────────────────────────────
DATA_PATH   = "data/online_retail_raw.csv"
OUTPUT_DIR  = "output"
SNAPSHOT    = datetime(2011, 12, 10)   # Reference date for recency calculation

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ── Load Data ──────────────────────────────────────────────────────────────────
print("Loading transaction data...")
df = pd.read_csv(DATA_PATH, parse_dates=["InvoiceDate"])
print(f"  {len(df):,} transactions | {df['CustomerID'].nunique():,} customers")

# ── RFM Calculation ────────────────────────────────────────────────────────────
print("\nCalculating RFM metrics...")

rfm = df.groupby("CustomerID").agg(
    LastPurchase=("InvoiceDate", "max"),
    Frequency=("InvoiceNo", "nunique"),
    Monetary=("TotalAmount", "sum")
).reset_index()

rfm["Recency"] = (SNAPSHOT - rfm["LastPurchase"]).dt.days

# Score each dimension 1–5 (5 = best)
rfm["R_Score"] = pd.qcut(rfm["Recency"],  5, labels=[5, 4, 3, 2, 1]).astype(int)
rfm["F_Score"] = pd.qcut(rfm["Frequency"].rank(method="first"), 5, labels=[1, 2, 3, 4, 5]).astype(int)
rfm["M_Score"] = pd.qcut(rfm["Monetary"], 5, labels=[1, 2, 3, 4, 5]).astype(int)
rfm["RFM_Score"] = rfm["R_Score"].astype(str) + rfm["F_Score"].astype(str) + rfm["M_Score"].astype(str)

# ── Segment Assignment ─────────────────────────────────────────────────────────
def assign_segment(row):
    r, f, m = row["R_Score"], row["F_Score"], row["M_Score"]
    if r >= 4 and f >= 4 and m >= 4:
        return "Champions"
    elif r >= 3 and f >= 3:
        return "Loyal Customers"
    elif r >= 4 and f <= 2:
        return "Potential Loyalists"
    elif r >= 3 and f <= 2 and m <= 2:
        return "Promising"
    elif r <= 2 and f >= 4:
        return "At Risk"
    elif r <= 2 and f >= 3 and m >= 4:
        return "Can't Lose Them"
    elif r <= 2 and f <= 2 and m >= 3:
        return "Hibernating"
    else:
        return "Lost"

rfm["Segment"] = rfm.apply(assign_segment, axis=1)

# ── Segment Summary ────────────────────────────────────────────────────────────
summary = rfm.groupby("Segment").agg(
    Customers=("CustomerID", "count"),
    Avg_Recency=("Recency", "mean"),
    Avg_Frequency=("Frequency", "mean"),
    Avg_Monetary=("Monetary", "mean"),
    Total_Revenue=("Monetary", "sum")
).round(2).reset_index()

total_revenue = rfm["Monetary"].sum()
summary["Revenue_Share_Pct"] = (summary["Total_Revenue"] / total_revenue * 100).round(1)

# ── Export ─────────────────────────────────────────────────────────────────────
rfm.to_csv(f"{OUTPUT_DIR}/rfm_segments.csv", index=False)
summary.to_csv(f"{OUTPUT_DIR}/segment_summary.csv", index=False)
print(f"\nExported: {OUTPUT_DIR}/rfm_segments.csv")
print(f"Exported: {OUTPUT_DIR}/segment_summary.csv")

# ── Console Summary ────────────────────────────────────────────────────────────
print("\n" + "="*60)
print("  CUSTOMER SEGMENTATION RESULTS")
print("="*60)
print(f"  Total Customers : {len(rfm):,}")
print(f"  Total Revenue   : ${total_revenue:,.0f}")
print(f"  Analysis Date   : {SNAPSHOT.date()}")
print("-"*60)

seg_order = ["Champions", "Loyal Customers", "Potential Loyalists",
             "Promising", "At Risk", "Can't Lose Them", "Hibernating", "Lost"]

for seg in seg_order:
    row = summary[summary["Segment"] == seg]
    if row.empty:
        continue
    row = row.iloc[0]
    print(f"  {seg:<22} {int(row['Customers']):>5} customers  "
          f"${row['Avg_Monetary']:>8,.0f} avg spend  "
          f"{row['Revenue_Share_Pct']:>5.1f}% of revenue")

print("="*60)
print("\nDone. Open dashboard/index.html to explore the results.\n")
