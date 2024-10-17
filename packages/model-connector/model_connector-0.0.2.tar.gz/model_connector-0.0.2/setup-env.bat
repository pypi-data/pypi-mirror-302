rem This script sets up the virtual environment for the project
rem It should be run from the root of the project
rem It is recommended to run the commands manually to ensure they are working as expected

rem Remove the environment if it exists
rmdir /S /Q .venv

rem Create and activate the environment
python -m venv .venv
if %errorlevel% neq 0 exit /b %errorlevel%

call .venv\Scripts\activate
if %errorlevel% neq 0 exit /b %errorlevel%

rem install the project
pip install -e .[dev]