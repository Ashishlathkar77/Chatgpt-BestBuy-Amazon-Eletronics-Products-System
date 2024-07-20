import streamlit as st
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import os
from config import openai_keys

# Set the OpenAI API key
os.environ['OPENAI_API_KEY'] = openai_keys

# Initialize the OpenAI model
llm = OpenAI(temperature=0.7)

# Define the prompt template for generating SQL queries
prompt_template = PromptTemplate(
    input_variables=["tables", "columns", "conditions"],
    template=(
        "Generate a complex SQL query involving the following tables: {tables}. "
        "Each table has the following columns: {columns}. "
        "Create a query with the following conditions: {conditions}."
    )
)

# Create an instance of LLMChain
sql_chain = LLMChain(
    llm=llm,
    prompt=prompt_template
)

# Streamlit UI
st.title("SQL Query Generator")

# Option to choose between single table and multiple tables
query_type = st.radio("Choose Query Type", ("Single Table", "Multiple Tables"))

if query_type == "Single Table":
    table_name = st.text_input("Table Name")
    columns = st.text_input("Columns (comma-separated)")
    conditions = st.text_area("Conditions")
    tables = table_name

elif query_type == "Multiple Tables":
    tables = st.text_area("Tables (comma-separated with optional JOIN conditions, e.g., 'users JOIN orders ON users.id = orders.user_id')")
    columns = st.text_area("Columns (comma-separated, e.g., 'users.id, users.name, orders.total')")
    conditions = st.text_area("Conditions (e.g., 'where users.points > 1000')")

# Generate SQL query when the button is pressed
if st.button("Generate SQL Query"):
    if not tables or not columns or not conditions:
        st.error("Please fill in all fields.")
    else:
        # Generate the SQL query
        result = sql_chain.invoke({
            "tables": tables,
            "columns": columns,
            "conditions": conditions
        })

        # Extract and display the SQL query
        sql_query = result.get('text', '').strip()
        st.write("Generated SQL Query:")
        st.code(sql_query, language='sql')

# Run the Streamlit app with `streamlit run app.py`
