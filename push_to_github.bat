@echo off

echo === Git Push Script ===
echo.

rem Check Git status
echo 1. Checking Git status...
git status
if %errorlevel% neq 0 (
    echo Error: Failed to check Git status
goto end
)
echo.

rem Add all modified files
echo 2. Adding all modified files...
git add .
if %errorlevel% neq 0 (
    echo Error: Failed to add files
goto end
)
echo.

rem Commit changes
echo 3. Committing changes...
git commit -m "Auto commit: Update code"
if %errorlevel% neq 0 (
    echo Error: Failed to commit changes
goto end
)
echo.

rem Push to GitHub
echo 4. Pushing to GitHub...
git push origin master --verbose
if %errorlevel% neq 0 (
    echo Error: Failed to push to GitHub
echo Please check your network connection or GitHub credentials
goto end
)
echo.

echo Success: Push completed!

:end
echo.
echo Press any key to exit...
pause >nul