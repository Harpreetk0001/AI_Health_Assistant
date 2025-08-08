**MedBuddy – Backend Prototype**

The backend API for MedBuddy, an AI-powered personal health assistant designed to support elderly care. This prototype provides RESTful endpoints to manage user data, health vitals, fall events, emergency contacts, and other core functionalities needed by the MedBuddy front-end application.

**Technologies Used:**
- Python 3.8+
- FastAPI – modern, fast (high-performance) web framework for building APIs
- SQLAlchemy – ORM for database modeling and interactions
- PostgreSQL – relational database
- Alembic – database migrations
- Uvicorn – ASGI server for running the FastAPI app

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

**Contribution:**
Always welcome for feedback and please feel free to open issues or submit pull requests to improve this backend prototype.

**Contact:**
For questions, reach out to hkb006@uowmail.edu.au
