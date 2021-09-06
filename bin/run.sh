PORT=30009
env/bin/python -m uvicorn app.main:app --host 0.0.0.0 --port ${PORT}