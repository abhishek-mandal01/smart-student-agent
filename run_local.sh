#!/bin/bash
source .venv/bin/activate
export $(cat .env | xargs)
streamlit run app.py
