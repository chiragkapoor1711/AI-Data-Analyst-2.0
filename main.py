import os
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
import sqlite3
from sqlalchemy import create_engine, inspect
import json
from dotenv import load_dotenv  # pip install python-dotenv

load_dotenv()  # .env file se API key lo

DB_URL = "sqlite:///amazone.db"
DB_PATH = "amazone.db"

def extract_schema(db_url: str) -> str:
    engine = create_engine(db_url)
    inspector = inspect(engine)
    schema = {}
    for table_name in inspector.get_table_names():
        columns = inspector.get_columns(table_name)
        schema[table_name] = [col['name'] for col in columns]
    return json.dumps(schema)

def get_model():
    return ChatGroq(
        model_name="llama-3.1-8b-instant",
        temperature=0,
        groq_api_key=os.getenv("GROQ_API_KEY")  # .env se lo
    )

def text_to_sql(schema: str, question: str, model) -> str:
    SYSTEM_PROMPT = """You are an SQL expert.
Convert the question into a valid SQL query.
Return ONLY the SQL query, no explanation, no markdown."""

    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("user", "Schema: {schema}\nQuestion: {question}\nSQL:")
    ])

    chain = prompt | model
    response = chain.invoke({"schema": schema, "question": question})

    # Markdown backticks clean karo agar model ne diye
    sql = response.content.strip()
    sql = sql.replace("```sql", "").replace("```", "").strip()
    return sql

def get_data(question: str, schema: str, model):
    sql_query = text_to_sql(schema, question, model)
    print("Generated SQL:", sql_query)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        result = cursor.execute(sql_query)
        columns = [desc[0] for desc in cursor.description]  # column names
        data = result.fetchall()
    finally:
        conn.close()

    return sql_query, columns, data