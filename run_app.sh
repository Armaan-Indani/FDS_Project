#!/bin/bash
echo "▶️ Running preprocessing..."
python preprocess.py

echo "✅ Preprocessing complete."
echo "🚀 Launching Streamlit app..."
streamlit run Home.py
