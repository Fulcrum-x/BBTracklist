@echo off
setlocal EnableDelayedExpansion

:CHECK_CREDENTIALS
python credential_setup.py check > temp.txt
set /p CRED_STATUS=<temp.txt
del temp.txt

if "%CRED_STATUS%"=="EXISTS" (
    :: Load existing credentials
    python credential_setup.py load > temp.txt
    for /f "tokens=1,* delims==" %%a in (temp.txt) do (
        if "%%a"=="CLIENT_ID" set SPOTIPY_CLIENT_ID=%%b
        if "%%a"=="CLIENT_SECRET" set SPOTIPY_CLIENT_SECRET=%%b
    )
    del temp.txt
    goto GET_ALBUM_INFO
) else (
    goto GET_CREDENTIALS
)

:GET_CREDENTIALS
cls
echo Album BBCode Generator Setup
echo ========================
echo.
echo First-time setup: Please enter your Spotify API credentials
echo These will be saved securely for future use.
echo.
set /p CLIENT_ID="Enter your Spotify Client ID: "
set /p CLIENT_SECRET="Enter your Spotify Client Secret: "

:: Save credentials securely
python credential_setup.py save "%CLIENT_ID%" "%CLIENT_SECRET%" > temp.txt
set /p SAVE_STATUS=<temp.txt
del temp.txt

if not "%SAVE_STATUS%"=="SUCCESS" (
    echo Error saving credentials!
    pause
    exit
)

:: Set environment variables
set SPOTIPY_CLIENT_ID=%CLIENT_ID%
set SPOTIPY_CLIENT_SECRET=%CLIENT_SECRET%

:GET_ALBUM_INFO
cls
echo Album Information
echo ================
echo.
set /p ARTIST="Enter artist name: "
set /p ALBUM="Enter album name: "

:RUN_SCRIPT
cls
echo Running BBCode Generator...
echo.

:: Run the Python script with the provided arguments
python album_bbcode.py "%ARTIST%" "%ALBUM%"

echo.
echo Attempting to copy to clipboard...
:: Copy the output to clipboard if the temp file exists
if exist temp_bbcode.txt (
    type temp_bbcode.txt | clip
    if errorlevel 1 (
        echo Failed to copy to clipboard!
    ) else (
        echo Successfully copied BBCode to clipboard!
    )
    del temp_bbcode.txt
) else (
    echo No BBCode file found to copy to clipboard!
)

echo.
echo ========================
echo Options:
echo 1. Generate another album
echo 2. Reset Spotify credentials
echo 3. Exit
echo.
set /p CHOICE="Enter your choice (1-3): "

if "%CHOICE%"=="1" goto GET_ALBUM_INFO
if "%CHOICE%"=="2" (
    python credential_setup.py delete
    goto GET_CREDENTIALS
)
if "%CHOICE%"=="3" exit