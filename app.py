import streamlit as st
import pandas as pd
from main import get_data, extract_schema, get_model, DB_URL

st.set_page_config(
    page_title="AI Data Analyst 2.0",
    page_icon="🤖",
    layout="wide"
)

# ✅ Cache - loads only once
@st.cache_resource
def load_model():
    return get_model()

@st.cache_data
def load_schema():
    return extract_schema(DB_URL)

model = load_model()
schema = load_schema()

# SIDEBAR
with st.sidebar:
    st.title("🤖 AI Data Analyst")
    st.markdown("---")
    st.markdown("### Features")
    st.markdown("""
    ✅ Natural language questions  
    ✅ AI-generated SQL  
    ✅ Auto data fetch  
    ✅ Smart analysis  
    """)
    st.markdown("---")
    st.info("Powered by Groq + LangChain + SQLite")

st.title("🤖 AI Data Analyst 2.0")
st.markdown("### Ask questions about your database in natural language")

user_query = st.text_area(
    "💬 Enter your question:",
    placeholder="Example: Show all customers from New York",
    height=120
)

if st.button("🚀 Analyze Data", use_container_width=True):
    if not user_query.strip():
        st.warning("⚠️ Please enter a question first.")
    else:
        with st.spinner("🔍 AI is analyzing your query..."):
            try:
                sql_query, columns, data = get_data(user_query, schema, model)

                st.success("✅ Analysis Complete!")

                # Show generated SQL
                with st.expander("🧠 View Generated SQL Query"):
                    st.code(sql_query, language="sql")

                st.markdown("## 📊 Query Result")

                if data:
                    df = pd.DataFrame(data, columns=columns)
                    st.dataframe(df, use_container_width=True)
                    st.caption(f"Total rows: {len(df)}")
                else:
                    st.info("No data found.")

            except Exception as e:
                st.error(f"❌ Error: {e}")
                st.info("Tip: Make sure the database file 'amazone.db' exists.")

st.markdown("---")
st.markdown("<center>Made By Chirag Kapoor", unsafe_allow_html=True)