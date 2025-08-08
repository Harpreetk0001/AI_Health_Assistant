**MedBuddy – Backend Prototype**

The backend API for MedBuddy, an AI-powered personal health assistant designed to support elderly care. This prototype provides RESTful endpoints to manage user data, health vitals, fall events, emergency contacts, and other core functionalities needed by the MedBuddy front-end application.

Technologies Used:
- Python 3.8+
- FastAPI – modern, fast (high-performance) web framework for building APIs
- SQLAlchemy – ORM for database modeling and interactions
- PostgreSQL – relational database
- Alembic – database migrations
- Uvicorn – ASGI server for running the FastAPI app

How to Run Backend Prototype:

1. Clone the repository
  Bash script-
   git clone https://github.com/yourusername/medbuddy-backend.git
   cd medbuddy-backend

2. Create and activate a virtual environment
  Bash script -
    python -m venv venv
    source venv/bin/activate    # Linux/macOS
    venv\Scripts\activate       # Windows

3. Install dependencies:
 Bash script -
    pip install -r requirements.txt

4. Configure environment variables:

  Create a .env file in the project root with your PostgreSQL connection string and other settings:
  Bash script -
    DATABASE_URL=postgresql://user:password@localhost/medbuddydb

5. Run database migrations:
  Bash script -
    alembic upgrade head

6. Start the backend server:
  Bash script -
    uvicorn app.main:app --reload

7. API Documentation
  Open your browser and navigate to:
  Bash script:
    http://localhost:8000/docs

 **API Overview**
  1.	Users: Create, read, update, delete user profiles.
  2.	Health Vitals: Store and retrieve health measurements (heart rate, hydration, sleep, etc.).
  3.	Fall Events: Record and access fall detection data.
  4.	Emergency Contacts: Manage emergency contact information.
  5.	Medication Schedule: Track medication reminders.
  6.	Other: Logs and AI-assisted suggestions.

**Project Structure**

app/
├── main.py            # FastAPI application entrypoint
├── models/            # Database models as User, HealthVital etc.
├── schemas/           # Pydantic schemas for request/response validation
├── crud/              # CRUD operation functions
├── api/               # API route definitions
├── db/                # Database connection setup
├── core/              # Configuration and security utilities
└── alembic/           # Database migration files

Contribution:
Always welcome for feedback and please feel free to open issues or submit pull requests to improve this backend prototype.

Contact:
For questions, reach out to hkb006@uowmail.edu.au
