@echo off
setlocal
set PYTHON_EXE=backend\venv\Scripts\python.exe

echo [docs] Step 1/4 Import latest source...
call sync_note.bat --no-pause
if errorlevel 1 exit /b 1

echo [docs] Step 2/4 Normalize document content...
"%PYTHON_EXE%" "backend\scripts\rewrite_documents_normalized.py"
if errorlevel 1 (
  echo [docs] FAILED during normalization.
  pause
  exit /b 1
)

echo [docs] Step 3/4 Apply manual refinements...
"%PYTHON_EXE%" "backend\scripts\manual_refine_documents.py"
if errorlevel 1 (
  echo [docs] FAILED during manual refine.
  pause
  exit /b 1
)

echo [docs] Step 4/4 Sync refined data to frontend...
"%PYTHON_EXE%" "backend\scripts\sync_frontend_data.py"
if errorlevel 1 (
  echo [docs] FAILED during final frontend sync.
  pause
  exit /b 1
)

echo [docs] ALL DONE.
pause
