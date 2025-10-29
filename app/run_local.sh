echo "Starting MedBuddy backend..."
# Detect Operating System
OS_TYPE="$(uname | tr '[:upper:]' '[:lower:]')"
# To activate virtual environment (if available)
if [ -d "venv" ]; then
    echo "Activating virtual environment..."
    if [[ "$OS_TYPE" == *"mingw"* || "$OS_TYPE" == *"msys"* || "$OS_TYPE" == *"cygwin"* ]]; then
        # Windows
        source venv/Scripts/activate
    else
        # Linux / macOS
        source venv/bin/activate
    fi
else
    echo "No virtual environment found. Creating one..."
    python3 -m venv venv
    if [[ "$OS_TYPE" == *"mingw"* || "$OS_TYPE" == *"msys"* || "$OS_TYPE" == *"cygwin"* ]]; then
        source venv/Scripts/activate
    else
        source venv/bin/activate
    fi
fi
# To check & install dependencies
echo "Checking dependencies..."
if [ -f "requirements.txt" ]; then
    echo "Installing dependencies from requirements.txt..."
    pip install --upgrade pip
    pip install -r requirements.txt
else
    echo "requirements.txt not found — installing core dependencies manually..."
    pip install fastapi uvicorn sqlalchemy alembic pydantic bcrypt python-jose[cryptography]
fi
# To verify Uvicorn installation
if ! command -v uvicorn &> /dev/null; then
    echo "Uvicorn not found — installing now..."
    pip install uvicorn
else
    echo "Uvicorn is already installed."
fi
# To start the FastAPI server
echo ""
echo "====================================="
echo "Environment ready!"
echo "Launching MedBuddy backend..."
echo "====================================="
echo ""
# To run server depending on OS
if [[ "$OS_TYPE" == *"mingw"* || "$OS_TYPE" == *"msys"* || "$OS_TYPE" == *"cygwin"* ]]; then
    echo "🪟 Detected Windows environment..."
    python -m uvicorn main:app --reload
else
    echo "Detected Linux/macOS environment..."
    uvicorn main:app --reload
fi
