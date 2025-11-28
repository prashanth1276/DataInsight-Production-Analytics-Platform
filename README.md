# DataInsight: Production Analytics Platform

A real-time business intelligence system that processes **11,672+ sales transactions worth $245,627** and delivers interactive insights using **FastAPI**, **PostgreSQL**, and **Power BI**.

---

## Dataset
Download from Kaggle: https://www.kaggle.com/datasets/mashlyn/online-retail-ii-uci . Once downloaded save it as online_retail.csv

After that Run this:
```bash
python utils/extract_sample.py
```
---

## Live Business Metrics

| Metric | Value |
|-------|-------|
| **Total Revenue** | **$245,627.58** |
| **Unique Customers** | **454** |
| **Product Catalog** | **2,109 items** |
| **Average Order Value** | **$21.04** |
| **Top Product** | *White Hanging Heart T-Light Holder* — **$5,251 revenue** |
| **Premium Customer** | Customer **#18102** — **$20,761 spend** |

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| **Backend** | FastAPI with Swagger/OpenAPI |
| **Database** | PostgreSQL (optimized indexed queries) |
| **ETL** | Pandas with **0.19s** batch processing |
| **Visualization** | Power BI |
| **Architecture** | Clean Architecture + Dependency Injection |

---

## Core API Endpoints (Sub-second responses)

| Endpoint | Server Processing | Description |
|----------|------------------|-------------|
| `GET /metrics/summary` | **40ms** | Key business metrics |
| `GET /metrics/top-products` | **39ms** | Product performance |
| `GET /metrics/sales-trend` | **40ms** | Revenue trends |
| `GET /metrics/customer-analysis` | **40ms** | Customer insights |

---

## Project Screenshots

| Feature | Screenshot |
|---------|-----------|
| API Documentation | `docs/api-documentation.png` |
| Business Revenue | `docs/business-metrics.png` |
| Top Products Report | `docs/top-products.png` |
| Power BI Dashboard | `docs/dashboard-complete.png` |
| KPIs | `docs/dashboard-kpis.png` |
| Running Server | `docs/server-running.png` |
etc..
---

## Quick Start

```bash
# 1. Clone repository
git clone https://github.com/prashanth1276/DataInsight-Production-Analytics-Platform
cd DataInsight-Production-Analytics-Platform

# 2. Create virtual environment
conda create -p datainsight_env Python==3.10
source conda activate datainsight_env/

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
# Update .env with PostgreSQL credentials

# 5. Verify Database (Optional)
python utils/verify_database.py

# 6. Run ETL process
python etl/etl_pipeline_optimized.py

# 7. Launch API server
python run_app.py

# 8. Open http://localhost:8000/docs
