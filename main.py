"""
Personal Finance Tracker API
FastAPI application connected to a PostgreSQL database (Supabase).

Run locally:
    pip install -r requirements.txt
    (create a .env file with DATABASE_URL – see .env.example)
    uvicorn main:app --reload
Then open http://127.0.0.1:8000/docs
"""
import os
from datetime import date
from decimal import Decimal

import psycopg
from psycopg.rows import dict_row
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

load_dotenv()  # reads DATABASE_URL from the .env file (never commit .env to GitHub)
DATABASE_URL = os.getenv("DATABASE_URL")

app = FastAPI(
    title="Personal Finance Tracker API",
    description="Stores income and expenses in PostgreSQL and returns simple reports.",
    version="1.0",
)


def run_query(sql, params=None):
    """Open a connection, run one query and return the rows as dictionaries."""
    with psycopg.connect(DATABASE_URL, row_factory=dict_row) as conn:
        with conn.cursor() as cur:
            cur.execute(sql, params)
            return cur.fetchall()


# ---------- Data ----------

@app.get("/categories")
def list_categories():
    return run_query("SELECT id, name, type FROM categories ORDER BY id;")


@app.get("/transactions")
def list_transactions():
    return run_query(
        """
        SELECT t.id, t.transaction_date, c.name AS category, c.type,
               t.amount, t.description
        FROM transactions t
        JOIN categories c ON t.category_id = c.id
        ORDER BY t.transaction_date;
        """
    )


class NewTransaction(BaseModel):
    category_id: int
    amount: Decimal = Field(gt=0, description="Must be greater than 0")
    description: str | None = Field(default=None, max_length=255)
    transaction_date: date


@app.post("/transactions", status_code=201)
def add_transaction(tx: NewTransaction):
    try:
        rows = run_query(
            """
            INSERT INTO transactions (category_id, amount, description, transaction_date)
            VALUES (%s, %s, %s, %s)
            RETURNING id, category_id, amount, description, transaction_date;
            """,
            (tx.category_id, tx.amount, tx.description, tx.transaction_date),
        )
    except psycopg.errors.ForeignKeyViolation:
        # the database itself rejects a category that does not exist
        raise HTTPException(status_code=400, detail="Category does not exist")
    return rows[0]


# ---------- Reports (the same SQL as sql/03_reports.sql) ----------

@app.get("/reports/monthly-totals")
def monthly_totals():
    return run_query(
        """
        SELECT TO_CHAR(t.transaction_date, 'YYYY-MM') AS month,
               c.type,
               SUM(t.amount) AS total
        FROM transactions t
        JOIN categories c ON t.category_id = c.id
        GROUP BY month, c.type
        ORDER BY month, c.type;
        """
    )


@app.get("/reports/by-category")
def spending_by_category(month: str = "2026-10"):
    """Spending per category for one month, e.g. ?month=2026-10"""
    return run_query(
        """
        SELECT c.name, SUM(t.amount) AS total
        FROM transactions t
        JOIN categories c ON t.category_id = c.id
        WHERE c.type = 'expense'
          AND TO_CHAR(t.transaction_date, 'YYYY-MM') = %s
        GROUP BY c.name
        ORDER BY total DESC;
        """,
        (month,),
    )


@app.get("/reports/net-trend")
def net_trend():
    return run_query(
        """
        SELECT TO_CHAR(t.transaction_date, 'YYYY-MM') AS month,
               SUM(CASE WHEN c.type = 'income' THEN t.amount
                        ELSE -t.amount END) AS net_balance
        FROM transactions t
        JOIN categories c ON t.category_id = c.id
        GROUP BY month
        ORDER BY month;
        """
    )
