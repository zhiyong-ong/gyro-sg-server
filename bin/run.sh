PORT=30009
env/bin/python -m uvicorn app.main:app --reload --host 0.0.0.0 --port ${PORT}