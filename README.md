# SQL Analytics Dashboard

A full-stack analytics dashboard that visualizes sales data from a PostgreSQL
database modeled on Microsoft's [AdventureWorks](https://learn.microsoft.com/en-us/sql/samples/adventureworks-install-configure)
sample dataset — KPIs, sales trends, top products, and territory breakdowns,
all filterable by date range and region.

## Problem

Business questions like "how's revenue trending this quarter" or "which
products are carrying the business" usually have an answer sitting in a
relational database — but getting to it means writing SQL, or waiting on
whoever can. That doesn't scale as a way for a team to check in on the
numbers, and it puts a technical bottleneck in front of a question that
should be self-serve.

## Solution

A dashboard that sits directly on top of the database and exposes the
common questions as interactive views: current totals, trend over time, top
performers, and a regional breakdown, all scoped by the same date-range and
territory filters. The backend does the aggregation in SQL (via SQLAlchemy,
not application-side loops), so the numbers stay fast and correct as the
dataset grows; the frontend turns them into charts a non-technical
stakeholder can explore without asking anyone for a query.

## Features

- **KPI summary** — total sales, total orders, average order value, and
  total customers, all filter-aware and shown as the first thing on the page
- **Sales-over-time** line chart, aggregated by month or week
- **Top 10 products by revenue**, with units sold, as a sortable table
- **Sales by territory**, with a bar/pie toggle for the same data
- **Date range + territory filtering** that scopes every chart and KPI at
  once, so the numbers always agree with each other
- **Graceful loading and empty states** — skeletons on first load; a filter
  change keeps the previous chart visible at reduced opacity instead of
  flashing back to a blank state; a friendly message when a filter
  combination has no matching data
- **Responsive layout**, from a single-column phone view up to a
  multi-column desktop layout
- **Seed script** that generates a realistic, AdventureWorks-styled dataset
  (10 sales territories, ~120 products across 4 categories, 300 customers,
  2,000 orders with line items) — useful for anyone cloning this repo
  without access to a real AdventureWorks database

## Tech stack

| Layer | Technology |
|---|---|
| Backend framework | [FastAPI](https://fastapi.tiangolo.com/) |
| ORM | [SQLAlchemy](https://www.sqlalchemy.org/) |
| Database | [PostgreSQL](https://www.postgresql.org/) |
| Backend language | Python |
| Frontend framework | [React](https://react.dev/) + [TypeScript](https://www.typescriptlang.org/) |
| Build tool | [Vite](https://vite.dev/) |
| Charts | [Recharts](https://recharts.org/) |
| Styling | [Tailwind CSS](https://tailwindcss.com/) |
| Sample data generation | [Faker](https://faker.readthedocs.io/) |

## Getting started

### 1. Database

Install PostgreSQL locally, then create the database:

```bash
createdb adventureworks_dashboard
```

### 2. Backend

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # adjust DATABASE_URL if needed
python3 seed.py        # creates tables and loads sample data
uvicorn main:app --reload
```

The API is now available at `http://localhost:8000` — try
`http://localhost:8000/health` or `http://localhost:8000/docs` for the
interactive API docs.

### 3. Frontend

```bash
cd frontend
npm install
npm run dev
```

The dashboard is now available at `http://localhost:5173`.

## Project structure

```
sql-analytics-dashboard/
├── backend/
│   ├── main.py          FastAPI app + /api endpoints
│   ├── models.py         SQLAlchemy models (Order, OrderDetail, Product, Customer, SalesTerritory)
│   ├── schemas.py         Pydantic response models
│   ├── database.py         Engine/session setup
│   ├── seed.py             Generates and loads sample data
│   └── requirements.txt
└── frontend/
    └── src/
        ├── api/            Typed API client
        ├── components/      Dashboard, filters, KPI cards, charts, table
        ├── lib/              Formatting helpers
        └── types/            Shared frontend types
```

## Screenshots

<!--
  Add screenshots here once the app is running with seeded data. See
  "Taking screenshots" below for guidance on what to capture. Suggested:

  ![Dashboard overview](./screenshots/overview.png)
  ![Sales trend and territory breakdown](./screenshots/charts.png)
  ![Mobile view](./screenshots/mobile.png)
-->

*(Screenshots coming soon.)*

## About this repository

This project was built iteratively with [Claude Code](https://claude.com/claude-code),
Anthropic's AI coding agent, as an AI-assisted development workflow: schema
design, API implementation, component architecture, and chart styling were
built through conversational, iterative prompts, with direction, review, and
final decisions made by the author at each step. It's included here as an
example of that workflow, not to claim the code was unsupervised — the
author reviewed, tested, and adjusted the output throughout.

## Author

**[Your name]**

[GitHub](https://github.com/your-username) · [LinkedIn](https://linkedin.com/in/your-profile) · [Portfolio](https://your-site.example)

*(Replace the placeholders above before publishing.)*
