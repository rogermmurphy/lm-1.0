@echo off
echo Setting up Git repository...
git rm --cached -f old/Ella-Ai
git commit -m "Clean initial commit"
git branch -M main
git push -f origin main
echo Done!
error: failed to push some refs to 'https://github.com/rogermmurphy/lm-1.0.git'