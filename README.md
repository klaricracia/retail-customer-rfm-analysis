# Customer RFM Segmentation & Loyalty Intelligence

> **CASE STUDY** · Retail Analytics · Python · SQL · Interactive Dashboard

---

## The Problem

Most retail teams know they have "good" customers and "bad" customers. What they don't know is which ones are about to leave, which ones are ready to spend more, and which ones are already gone.

Without that clarity, marketing budgets get spread equally across customers who behave very differently — and the teams with the highest lifetime value get the same email as customers who bought once three years ago.

This project builds a data-driven customer segmentation system using **RFM (Recency, Frequency, Monetary)** analysis to answer one question:

> *Which customers deserve your attention right now, and what action should you take with each?*

---

## Approach

### 1. Data & Cleaning
- Dataset: 32,000+ retail transactions across 4,338 unique customers
- Removed cancelled orders, missing customer IDs, and negative quantities
- Established a snapshot date (Dec 10, 2011) as the recency reference point

### 2. RFM Scoring
Each customer receives three scores (1–5 scale, 5 = best):

| Dimension | Definition | Signal |
|-----------|-----------|--------|
| **Recency (R)** | Days since last purchase | Is this customer active? |
| **Frequency (F)** | Number of unique orders | Do they come back? |
| **Monetary (M)** | Total spend | How much do they contribute? |

Scores are calculated using quantile-based bucketing so that rankings are relative to the actual customer base — not fixed thresholds.

### 3. Segment Assignment
RFM scores are combined into 8 business-meaningful segments with specific retention actions:

| Segment | Profile | Action |
|---------|---------|--------|
| **Champions** | High R, F, M | Reward & upsell |
| **Loyal Customers** | Strong F & M, moderate R | Loyalty programme |
| **At Risk** | High F & M historically, low R | Win-back campaign |
| **Can't Lose Them** | Very high M, not returning | Personal outreach |
| **Potential Loyalists** | Recent, low frequency | Onboard & nurture |
| **Promising** | Moderate R, low F | Build relationship |
| **Hibernating** | Low R, some history | Last-chance offer |
| **Lost** | Low across all dimensions | Re-engage or sunset |

### 4. Dashboard
Results are visualized in a branded interactive dashboard covering:
- KPI summary (total revenue, customers, revenue concentration)
- Customer distribution by segment (donut chart)
- Revenue by segment (horizontal bar)
- Recency vs. spend matrix (bubble chart)
- Full segment table with recommended actions

---

## Stack

```
Python · pandas · numpy · HTML/CSS/JS · Chart.js
```

**Core libraries:**
- `pandas` — data wrangling, groupby aggregations, quantile scoring
- `numpy` — numerical operations
- `Chart.js` — interactive dashboard charts (no external dependencies)

---

## Results

| Metric | Value |
|--------|-------|
| Total customers analyzed | 4,338 |
| Total revenue in dataset | $12.1M |
| Champions (top segment) | 1,072 customers · 56.5% of revenue |
| At-risk revenue exposure | $1.6M from 186 high-value customers |
| Lost customers identified | 1,534 — eligible for re-engagement or suppression |

**Key insight:** 24.7% of customers (Champions) generate 56.5% of total revenue. The At Risk segment — just 186 customers — represents $1.6M in revenue that is actively at risk of churn. A targeted win-back campaign for this cohort alone justifies the entire analytical investment.

---

## What I Learned

**On the data side:** RFM is deceptively simple — the complexity is in the segment definitions. Where you draw the boundary between "Loyal" and "At Risk" has real commercial consequences, and those thresholds should be calibrated per business, not copied from a template.

**On the business side:** The most actionable insight wasn't the Champions (every team already knows who their best customers are). It was the At Risk segment — high-frequency, high-spend customers who have gone quiet. That's the fire worth putting out.

**On the technical side:** Quantile-based scoring is more robust than fixed thresholds, but it means scores are relative — a score of 5 means "top 20% of your customers," not "great customer by some absolute standard." Always communicate this caveat to stakeholders.

---

## How to Run

```bash
# Clone the repo
git clone https://github.com/klaricracia/retail-customer-rfm-analysis.git
cd retail-customer-rfm-analysis

# Install dependencies
pip install pandas numpy openpyxl

# Run the analysis
python rfm_analysis.py

# Open the dashboard
open dashboard/index.html
```

Output files are written to `/output`:
- `rfm_segments.csv` — one row per customer with RFM scores and segment label
- `segment_summary.csv` — aggregated metrics per segment

---

## How to Extend This

- **Automate it:** Schedule `rfm_analysis.py` to run weekly and track segment migration over time
- **Add churn probability:** Layer a logistic regression on top of RFM scores to predict churn likelihood
- **Connect to CRM:** Export segment labels to your CRM or email platform for automated campaign triggers
- **Add cohort analysis:** Track what percentage of each month's new customers become Champions within 12 months

---

*Built by [Klarissa Artavia](https://www.linkedin.com/in/klariartavia/) · Data & AI Strategy*
*GitHub: [github.com/klaricracia](https://github.com/klaricracia)*
