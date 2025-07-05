@echo off
echo Starting Dream Journal AI...
echo.
echo Installing dependencies...
pip install -r requirements.txt
echo.
echo Setting up NLTK data...
python setup_nltk.py
echo.
echo Starting the application...
echo Open your browser and go to: http://localhost:5000
echo.
python app.py
pause
