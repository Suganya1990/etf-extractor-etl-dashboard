# ETF Holdings Tracker (URNM, URNJ) — v1

## North Star
See how URNM and URNJ holdings change over time, every day, with clear visuals of new/removed positions and weight deltas.

## Scope (v1)
- **ETFs:** URNM, URNJ
- **What I ship:** 
  - **DB:** SQL Server schema with core + marts (scripts in /sql)
  - **ETL:** Python jobs to fetch, validate, and load daily snapshots (/src)
  - **Power BI:** A report to visualize holdings and day-over-day changes (/bi/ETF_Tracker.pbix)
  - **Docs:** README, ERD, pipeline diagram, data dictionary, runbook (/docs)
  - **Tests:** Unit + integration tests with sample data (/tests)
- **Out of scope (v1):** Intraday prices, non-daily cadences, options/derivatives parsing

## Quickstart
1. Create DB: run `sql/01_core_tables.sql` then `sql/03_marts.sql`.
2. Setup env: `python -m venv .venv && .venv/Scripts/pip install -r requirements.txt`
3. Configure `.env` from `.env.example`.
4. Run once: `python src/jobs/daily_pipeline.py`
5. Open `bi/ETF_Tracker.pbix` and connect to the DB (mart schema).

## Operations
- Daily schedule: 7:30pm ET via Task Scheduler.
- Logs in `/logs`; failures send a webhook alert.
