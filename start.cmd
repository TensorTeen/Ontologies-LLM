cd .\apache-jena-fuseki-5.0.0-rc1
start fuseki-server.bat
cd ..
start streamlit run app.py
start ngrok http 8501