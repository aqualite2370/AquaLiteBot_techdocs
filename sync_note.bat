@echo off
setlocal
set SHARE_URL=https://share.note.youdao.com/ynoteshare/index.html?id=640449dc469077ec5ed8437e115b925a^&type=notebook^&_time=1775739900258
set PYTHON_EXE=backend\venv\Scripts\python.exe
set SCRIPT=backend\scripts\import_youdao_share.py
set MIN_DOCS=1
set MIN_RATIO=0.2

echo [sync] Importing Youdao notebook...
"%PYTHON_EXE%" "%SCRIPT%" "%SHARE_URL%" --min-docs %MIN_DOCS% --min-ratio %MIN_RATIO%
if errorlevel 1 (
  echo [sync] FAILED. Existing documents.json kept untouched.
  echo [sync] You can tune MIN_DOCS/MIN_RATIO at the top of sync_note.bat if you intentionally removed many notes.
  pause
  exit /b 1
)

echo [sync] SUCCESS.
pause
