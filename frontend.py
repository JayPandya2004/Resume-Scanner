import streamlit as st
import requests

st.title("Resume Ranking App")
job_desc = st.text_area("Enter Job Description")

uploaded_files = st.file_uploader("Upload Resumes (PDF)", type=["pdf"], accept_multiple_files=True)

if st.button("Rank Candidates"):
    with st.spinner("Processing..."):
        files = [("resumes", (f.name, f, "application/pdf")) for f in uploaded_files]
        res = requests.post("http://localhost:5000/rank", files=files, data={"job_description": job_desc})
        
        if res.status_code == 200:
            results = res.json()
            for result in results:
                st.subheader(f"Rank {result['rank']} - Score: {result['score']:.2f}")
                st.write(result['data'])
        else:
            st.error("Error from backend.")
