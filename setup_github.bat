@echo off
echo Setting up Git repository...
git rm --cached -f old/Ella-Ai
git commit -m "Clean initial commit"
git branch -M main
git push -f origin main
echo Done!
