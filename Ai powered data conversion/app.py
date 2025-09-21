import streamlit as st
from langchain.llms import Ollama
import json
import pandas as pd

# Example prompt section
EXAMPLES = """
Example 1:
FlatFile: 00022ABRIGHT FUTURE 00002234500233455 S MAIN STREET-CHICAGO- -1000000012000002300000034000004500000065000000670000
Student Academic Notes Data1Data2
JSON:
{
  "customerId": "00022ABRIGHT FUTURE",
  "companyName": "BRIGHT FUTURE",
  "accountCode": "00002234500233455",
  "statusFlag": "S",
  "address": "MAIN STREET",
  "city": "CHICAGO",
  "stateCountry": "ILUSA",
  "numericData": [1000000012,23,340,450,560,670,780,890],
  "occupation": "STUDENT",
  "notes": "ACADEMIC NOTES",
  "extraData": "DATA1DATA2"
}
"""

EXAMPLES2 = """
Example 2:
"input": {
    "headers": ["EMPLOYEE_ID", "EMPLOYEE_NAME", "DEPT_ID", "SALARY", "JOIN_DATE"],
    "row": ["1106", "Linda Thomas", "D30", "93000", "2020-11-05"]
}
output_json:
{
  "EMPLOYEE_ID": "1106",
  "EMPLOYEE_NAME": "Linda Thomas",
  "DEPT_ID": "D30",
  "SALARY": "93000",
  "JOIN_DATE": "2020-11-05"
}
"""

llm = Ollama(model="mistral")  # Replace with your model name

def parse_uploaded_file(file, file_type):
    if file_type == "csv":
        df = pd.read_csv(file)
        headers = df.columns.tolist()
        row = df.iloc[0].astype(str).tolist()
    else:
        content = file.read().decode("utf-8")
        lines = [line.strip() for line in content.splitlines() if line.strip()]
        headers = lines[0].split()
        row = lines[1].split() if len(lines) > 1 else []
    return {"headers": headers, "row": row}

def generate_prompt(input_text):
    return f"""
{EXAMPLES}

Now convert this input record into JSON format:
FlatFile: {input_text}
JSON:
"""

def generate_prompt_db2(table_data):
    return f"""{EXAMPLES2}

Now convert this input record into JSON format:
"input": {json.dumps(table_data)}
output_json:
"""

import streamlit as st

def dashboard():
    st.markdown(
        "<h1 style='text-align: center; color: #06bcee; font-size: 3em; font-weight: bold;'>AI-Powered Data Processing App</h1>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<h4 style='text-align:center; color:#C0C7D1; margin-top:-0.5em;'>Modernize legacy data pipelines by converting flat files and database extracts into clean, structured JSON.</h4>",
        unsafe_allow_html=True,
    )

    st.markdown("---")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📄 Flat File Upload")
        st.write(
            "Upload and transform complex legacy flat files into structured JSON with ease. "
            "Powered by advanced AI extraction and error correction."
        )
    with col2:
        st.subheader("🗃️ CSV & DB2 Integration")
        st.write(
            "Import, preview, and process CSV or DB2 data extracts. "
            "Everything is fast and interactive. See, check, and convert your tables instantly!"
        )

    st.markdown("---")
    st.subheader("🚀 Why use this app?")
    st.markdown(
        """
        - **Instant Modernization:** No code. Just upload and go.
        - **Robust Error Handling:** See detailed feedback if something doesn't parse.
        - **AI-Augmented Flexibility:** Convert both structured and semi-structured records.
        """
    )
    st.info("Use the sidebar to select Flat Files or DB2 Files and get started!")





def flat_files_page():
    st.title("Flat Files Upload & Processing")
    uploaded_file = st.file_uploader("Upload .txt file", type=["txt"])
    if uploaded_file:
        file_content = uploaded_file.read().decode("utf-8")
        st.subheader("File Content Preview")
        st.text(file_content)
        if st.button("Convert to JSON"):
            prompt = generate_prompt(file_content)
            st.write("Processing")
            try:
                output = llm(prompt)
                try:
                    json_output = json.loads(output)
                    st.subheader("LLM JSON Output:")
                    st.json(json_output)
                except json.JSONDecodeError:
                    st.subheader("LLM raw output:")
                    st.text(output)
            except Exception as e:
                st.error(f"Error querying Ollama LLM: {e}")

def db2_files_page():
    st.title("DB2 Files (CSV) Upload and Processing")
    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
    if uploaded_file:
        table_data = parse_uploaded_file(uploaded_file, "csv")
        st.subheader("Parsed Table Data")
        st.json(table_data)
        if st.button("Convert with LLM"):
            prompt = generate_prompt_db2(table_data)
            # st.code(prompt)
            try:
                response = llm(prompt)
                try:
                    st.subheader("LLM JSON Output")
                    output_json = json.loads(response)
                    st.json(output_json)
                except json.JSONDecodeError:
                    st.subheader("Raw LLM Output")
                    st.text(response)
            except Exception as e:
                st.error(f"Error calling LLM: {e}")

def main():
    st.sidebar.title("Navigation")
    choice = st.sidebar.selectbox("Choose page", ["Dashboard", "Flat Files", "DB2 Files"])

    if choice == "Dashboard":
        dashboard()
    elif choice == "Flat Files":
        flat_files_page()
    elif choice == "DB2 Files":
        db2_files_page()

if __name__ == "__main__":
    main()
