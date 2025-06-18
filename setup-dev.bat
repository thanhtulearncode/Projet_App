@echo off
echo 🚀 Setting up Wall Street Game for local development...

REM Backend setup
echo 📦 Setting up backend...
cd backend
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Installing backend dependencies...
pip install -r requirements.txt

echo ✅ Backend setup complete!

REM Frontend setup
echo 📦 Setting up frontend...
cd ..\frontend

echo Installing frontend dependencies...
npm install

echo ✅ Frontend setup complete!

echo.
echo 🎉 Setup complete! To start development:
echo.
echo Backend (Command Prompt 1):
echo   cd backend
echo   venv\Scripts\activate
echo   uvicorn api:app --reload
echo.
echo Frontend (Command Prompt 2):
echo   cd frontend
echo   npm start
echo.
echo 🌐 Open http://localhost:3000 to play!
pause 