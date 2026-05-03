@echo off
setlocal EnableDelayedExpansion

cd /d "%~dp0"

set "PYTHON_EXE=backend\venv\Scripts\python.exe"
set "SHARE_URL=https://share.note.youdao.com/ynoteshare/index.html?id=640449dc469077ec5ed8437e115b925a&type=notebook&_time=1775739900258"
set "IMPORT_SCRIPT=backend\scripts\import_youdao_share.py"
set "NORMALIZE_SCRIPT=backend\scripts\rewrite_documents_normalized.py"
set "REFINE_SCRIPT=backend\scripts\manual_refine_documents.py"
set "SYNC_SCRIPT=backend\scripts\sync_frontend_data.py"
set "MIN_DOCS=1"
set "MIN_RATIO=0.2"

if not exist "%PYTHON_EXE%" set "PYTHON_EXE=python"

echo [publish] Step 1/7 Check git repository...
git rev-parse --is-inside-work-tree >nul 2>nul
if errorlevel 1 (
  echo [publish] Current folder is not a git repository.
  pause
  exit /b 1
)

echo [publish] Step 2/7 Import latest Youdao notes...
"%PYTHON_EXE%" "%IMPORT_SCRIPT%" "%SHARE_URL%" --min-docs %MIN_DOCS% --min-ratio %MIN_RATIO%
if errorlevel 1 (
  echo [publish] Import failed. Existing documents.json should remain untouched.
  pause
  exit /b 1
)

echo [publish] Step 3/7 Normalize document content...
"%PYTHON_EXE%" "%NORMALIZE_SCRIPT%"
if errorlevel 1 (
  echo [publish] Normalize failed.
  pause
  exit /b 1
)

echo [publish] Step 4/7 Apply manual refinements...
"%PYTHON_EXE%" "%REFINE_SCRIPT%"
if errorlevel 1 (
  echo [publish] Manual refine failed.
  pause
  exit /b 1
)

echo [publish] Step 5/7 Sync frontend static data...
"%PYTHON_EXE%" "%SYNC_SCRIPT%"
if errorlevel 1 (
  echo [publish] Frontend data sync failed.
  pause
  exit /b 1
)

echo [publish] Step 6/7 Stage generated document data...
git add -- backend/data/documents.json frontend/public/data/documents.json
if errorlevel 1 (
  echo [publish] git add failed.
  pause
  exit /b 1
)

git diff --cached --quiet
if not errorlevel 1 (
  echo [publish] No staged changes detected. Nothing to commit.
  pause
  exit /b 0
)

set "COMMIT_MESSAGE=Update docs %date% %time%"

git commit -m "%COMMIT_MESSAGE%"
if errorlevel 1 (
  echo [publish] git commit failed.
  pause
  exit /b 1
)

echo [publish] Step 7/7 Push to GitHub...
for /f "usebackq tokens=*" %%b in (`git branch --show-current`) do set "CURRENT_BRANCH=%%b"
if "%CURRENT_BRANCH%"=="" (
  echo [publish] Cannot detect current branch.
  pause
  exit /b 1
)

git push -u origin "%CURRENT_BRANCH%"
if errorlevel 1 (
  echo [publish] git push failed. Your commit is still saved locally.
  pause
  exit /b 1
)

echo [publish] All done.
pause
