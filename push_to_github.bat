@echo off

rem Check Git status
git status

rem Add all modified files
git add .

rem Commit changes
git commit -m "Auto commit: Update code"

rem Push to GitHub
git push origin master

echo Push completed!
pause