import requests
from .database import initialize_database, run_readonly_query
from .retriever import DocumentRetriever
from .config import OLLAMA_URL, OLLAMA_MODEL

SQL_GUIDANCE = """
You are a SQL planner for a SQLite sales database. Table sales columns:
id, order_date, region, product, category, quantity, revenue, cost, customer_segment.
Return ONLY one read-only SQLite SELECT query. Never modify data. If the question is not answerable from this table, return:
SELECT * FROM sales LIMIT 0;
"""

class BusinessIntelligenceAssistant:
    def __init__(self):
        initialize_database()
        self.retriever = DocumentRetriever()
        self.retriever.load_or_build()

    def rebuild_index(self):
        self.retriever.rebuild()

    def _ollama(self, prompt):
        response = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json={"model": OLLAMA_MODEL, "prompt": prompt, "stream": False},
            timeout=120,
        )
        response.raise_for_status()
        return response.json().get("response", "").strip()

    def _plan_sql(self, question):
        try:
            sql = self._ollama(SQL_GUIDANCE + "\nQuestion: " + question + "\nSQL:")
            sql = sql.replace("```sql", "").replace("```", "").strip()
            if sql.lower().startswith("sql"):
                sql = sql[3:].strip()
            return sql
        except requests.RequestException:
            return "SELECT * FROM sales LIMIT 0;"

    def ask(self, question):
        sources = self.retriever.search(question)
        sql = self._plan_sql(question)
        try:
            df = run_readonly_query(sql)
            records = df.head(30).to_dict(orient="records")
        except Exception:
            records, sql = [], "SQL query rejected or could not be executed."
        context = "\n\n".join(
            f"[Document: {s['source']} | similarity: {s['score']:.3f}]\n{s['text']}"
            for s in sources
        )
        evidence = str(records)
        prompt = f"""You are a careful business intelligence analyst.
Answer the user's question using ONLY the evidence below. If evidence is insufficient,
say what is missing. Do not invent metrics. Clearly distinguish document evidence from
database records. Mention relevant dates and units.

QUESTION:
{question}

RETRIEVED DOCUMENTS:
{context or "No relevant document chunks found."}

SQL RECORDS:
{evidence or "No matching SQL records."}

ANSWER:"""
        try:
            answer = self._ollama(prompt)
        except requests.RequestException:
            answer = ("The local LLM is not reachable. Start Ollama and run "
                      f"`ollama pull {OLLAMA_MODEL}`. Retrieved evidence is available below.")
        return {"answer": answer, "sources": sources, "records": records, "sql": sql}
