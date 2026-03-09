import streamlit as st

st.title("Medi-Flow Orchestrator")

transcript = st.text_area("Doctor Transcript")

if st.button("Analyze"):
    st.write("AI detected hahahah:")
    st.write("Blood Test → Laboratory")
    st.write("Paracetamol → Pharmacy")
