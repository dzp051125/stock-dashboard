@echo off
setlocal
cd /d "%~dp0frontend"

rem Use installed tools first, then the available Codex runtime.
set "DASHBOARD_RUNTIME=%USERPROFILE%\.cache\codex-runtimes\codex-primary-runtime\dependencies"
where node >nul 2>&1
if errorlevel 1 (
  if not exist "%DASHBOARD_RUNTIME%\node\bin\node.exe" (
    echo Node.js was not found. Install Node.js or restore the local runtime.
    exit /b 1
  )
  set "PATH=%DASHBOARD_RUNTIME%\node\bin;%PATH%"
)

where pnpm >nul 2>&1
if errorlevel 1 (
  if not exist "%DASHBOARD_RUNTIME%\bin\fallback\pnpm.cmd" (
    echo pnpm was not found. Install pnpm or restore the local runtime.
    exit /b 1
  )
  set "PATH=%DASHBOARD_RUNTIME%\bin\fallback;%PATH%"
)

call pnpm dev
exit /b %ERRORLEVEL%
