from fastapi import FastAPI
from pydantic import BaseModel
from app.snowflake_client import get_session

app = FastAPI(title="Snowflake Analytics API")

# ---------- Health Check ----------
@app.get("/health")
def health():
    return {"status": "ok"}

# ---------- Predefined Analytics ----------
@app.post("/analytics")
def analytics(report: dict):
    session = get_session()

    report_type = report.get("type")

    if report_type == "total_sales_per_customer":
        df = session.sql("""
            SELECT
                c.CUSTOMER_NAME,
                SUM(s.AMOUNT) AS TOTAL_SALES
            FROM CUSTOMERS c
            JOIN SALES s ON c.CUSTOMER_ID = s.CUSTOMER_ID
            GROUP BY c.CUSTOMER_NAME
            ORDER BY TOTAL_SALES DESC
        """)
        return df.to_pandas().to_dict(orient="records")

    return {"error": "Unknown report type"}

# ---------- Natural Language ----------
class Question(BaseModel):
    question: str

@app.post("/ask")
def ask(q: Question):
    session = get_session()

    result = session.sql(f"""
        SELECT *
        FROM TABLE(
            CORTEX_ANALYST(
                'SHIVANSHI_SEMANTIC_VIEW',
                '{q.question}'
            )
        )
    """)

    return result.to_pandas().to_dict(orient="records")
