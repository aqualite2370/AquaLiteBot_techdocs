@echo off
setlocal EnableDelayedExpansion

cd /d "%~dp0"

set PUSH_AFTER=
set COMMIT_MESSAGE=

echo [publish] Step 1/4 Update docs and sync frontend data...
call "更新文档并同步前端.bat"
if errorlevel 1 exit /b 1

echo [publish] Step 2/4 Check git repository...
git rev-parse --is-inside-work-tree >nul 2>nul
if errorlevel 1 (
  echo [publish] Current folder is not a git repository.
  pause
  exit /b 1
)

echo [publish] Step 3/4 Stage changes...
git add .
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
set /p COMMIT_MESSAGE=[publish] Commit message ^(Enter to use default^): 
if "%COMMIT_MESSAGE%"=="" set "COMMIT_MESSAGE=Update docs %date% %time%"

git commit -m "%COMMIT_MESSAGE%"
if errorlevel 1 (
  echo [publish] git commit failed.
  pause
  exit /b 1
)

set /p PUSH_AFTER=[publish] Push to GitHub now? ^(y/N^): 
if /I "%PUSH_AFTER%"=="y" goto push_now
if /I "%PUSH_AFTER%"=="yes" goto push_now

echo [publish] Commit created locally. You can push later with: git push
pause
exit /b 0

:push_now
echo [publish] Step 4/4 Push to remote...
git push
if errorlevel 1 (
  echo [publish] git push failed. Your commit is still saved locally.
  pause
  exit /b 1
)

echo [publish] All done.
pause
