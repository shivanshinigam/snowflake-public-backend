from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.snowflake_client import get_session

app = FastAPI(title="Snowflake Analytics API")

# ---------- Health Check ----------
@app.get("/health")
def health():
    return {"status": "ok"}


# ---------- Analytics Request Model ----------
class AnalyticsRequest(BaseModel):
    type: str
    customer: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None


# ---------- Predefined Analytics ----------
@app.post("/analytics")
def analytics(report: AnalyticsRequest):
    session = get_session()

    try:
        if report.type == "total_sales_per_customer":

            query = """
                SELECT
                    c.CUSTOMER_NAME,
                    SUM(s.AMOUNT) AS TOTAL_SALES
                FROM CUSTOMERS c
                JOIN SALES s ON c.CUSTOMER_ID = s.CUSTOMER_ID
                WHERE 1=1
            """

            # Optional filters
            if report.customer:
                query += f" AND c.CUSTOMER_NAME = '{report.customer}'"

            if report.start_date:
                query += f" AND s.ORDER_DATE >= '{report.start_date}'"

            if report.end_date:
                query += f" AND s.ORDER_DATE <= '{report.end_date}'"

            query += """
                GROUP BY c.CUSTOMER_NAME
                ORDER BY TOTAL_SALES DESC
            """

            df = session.sql(query)
            return df.to_pandas().to_dict(orient="records")

        else:
            raise HTTPException(
                status_code=400,
                detail=f"Unknown analytics type: {report.type}"
            )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ---------- Natural Language ----------
class Question(BaseModel):
    question: str


@app.post("/ask")
def ask(q: Question):
    session = get_session()

    try:
        result = session.sql(
            f"""
            SELECT *
            FROM TABLE(
                CORTEX_ANALYST(
                    'SHIVANSHI_SEMANTIC_VIEW',
                    '{q.question}'
                )
            )
            """
        )
        return result.to_pandas().to_dict(orient="records")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
