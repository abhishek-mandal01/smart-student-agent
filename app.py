import streamlit as st
from src.orchestrator import run_session
from src.memory import memory
from src.config import settings
import os

st.set_page_config(page_title="Smart Student Agent", layout="wide")

st.title("Smart Student Productivity Agent — Demo")

user_id = st.text_input("User ID", settings.DEFAULT_USER_ID)

uploaded_files = st.file_uploader("Upload lecture PDFs", accept_multiple_files=True, type=["pdf"])
if st.button("Run study session"):
    if not uploaded_files:
        st.warning("Upload at least one PDF to run the demo (or place sample PDF in project).")
    else:
        # Save uploaded files temporarily
        paths = []
        for f in uploaded_files:
            local_path = os.path.join("tmp", f.name)
            os.makedirs("tmp", exist_ok=True)
            with open(local_path, "wb") as out:
                out.write(f.getbuffer())
            paths.append(local_path)
        with st.spinner("Running agents..."):
            out = run_session(user_id, paths)
            st.subheader("Summary")
            st.write(out["summary"])
            st.subheader("Quiz")
            for i, q in enumerate(out["quiz"]):
                st.markdown(f"**Q{i+1}:** {q.get('q')}")
                for opt in q.get("options", []):
                    st.write(f"- {opt}")
