@echo off
title GaiAI
color 0A

cd %~dp0

echo Configuration files checked.

echo Checking dependencies...
if exist "..\node_modules" (
    echo Using node_modules from parent directory...
    cd ..
    CALL pip install -r requirements.txt
    cd %~dp0
) else (
    echo Installing dependencies in current directory...
    CALL pip install -r requirements.txt
)
echo Dependencies installation completed!
title GaiAI
echo Starting the bot...
python bot.py

pause
exit
