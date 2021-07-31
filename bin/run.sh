PORT=8282
uvicorn app.main:app --reload --host 0.0.0.0 --port ${PORT}