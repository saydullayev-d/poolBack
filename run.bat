@echo off
cd C:\\Users\\Damir\\poolBack
call .\\venv\\Scripts\\activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 6577