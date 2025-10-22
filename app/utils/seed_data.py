from app.core.database import SessionLocal, engine
from app.core.database import Base
from app.core.config import settings
from app.core.security import get_password_hash
from app import crud, models
import datetime

def create_all():
    Base.metadata.create_all(bind=engine)

def seed_example():
    db = SessionLocal()
    try:
        # create default user
        existing = db.query(models.User).filter(models.User.email == "demo@example.com").first()
        if not existing:
            u = models.User(email="demo@example.com", hashed_password=get_password_hash("password"))
            db.add(u); db.commit(); db.refresh(u)
        else:
            u = existing

        # vitals
        for i in range(3):
            v = models.Vitals(
                user_id=u.id,
                hydration=50 + i,
                sleep=7 + i*0.1,
                heartbeat=70 + i,
                bp_systolic=120 + i,
                bp_diastolic=80 + i,
                steps=1000 + i*100,
                timestamp=datetime.datetime.utcnow() - datetime.timedelta(days=3-i)
            )
            db.add(v)
        # tasks
        t = models.Task(user_id=u.id, title="Take morning meds", description="Medication A", tag="Medication", status="Incomplete")
        db.add(t)
        # contact
        c = models.Contact(user_id=u.id, name="Alice", relationship="Daughter", phone="123456", email="alice@example.com", favourite=True)
        db.add(c)
        db.commit()
    finally:
        db.close()

if __name__ == "__main__":
    create_all()
    seed_example()
    print("Seeded example data")
