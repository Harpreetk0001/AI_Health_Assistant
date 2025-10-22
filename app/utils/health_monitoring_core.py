from typing import List, Tuple, Optional, Any
import datetime
from sqlalchemy.orm import Session

# in-memory matrices (global)
VitalsMatrix: Tuple[List, List, List, List, List, List] = ([], [], [], [], [], [])
TimeStamps: List[datetime.datetime] = []

# Defensive imports
try:
    from app import crud
    from app import models
except Exception:
    crud = None
    models = None


class Vitals:
    """
    Vitals object:
      hydration, sleep, hb, bp_systolic, bp_diastolic, steps, timestamp
    When instantiated -> appended into VitalsMatrix and TimeStamps.
    """
    def __init__(
        self,
        hydration: Optional[float] = None,
        sleep: Optional[float] = None,
        hb: Optional[float] = None,
        bp_systolic: Optional[float] = None,
        bp_diastolic: Optional[float] = None,
        steps: Optional[int] = None,
        timestamp: Optional[datetime.datetime] = None,
    ):
        self.hydration = hydration
        self.sleep = sleep
        self.hb = hb
        self.bp_systolic = bp_systolic
        self.bp_diastolic = bp_diastolic
        self.steps = steps
        self.timestamp = timestamp or datetime.datetime.utcnow()

        # append to global matrices
        VitalsMatrix[0].append(self.hydration)
        VitalsMatrix[1].append(self.sleep)
        VitalsMatrix[2].append(self.hb)
        VitalsMatrix[3].append(self.bp_systolic)
        VitalsMatrix[4].append(self.bp_diastolic)
        VitalsMatrix[5].append(self.steps)
        TimeStamps.append(self.timestamp)

    def as_dict(self):
        return {
            "hydration": self.hydration,
            "sleep": self.sleep,
            "heartbeat": self.hb,
            "bp_systolic": self.bp_systolic,
            "bp_diastolic": self.bp_diastolic,
            "steps": self.steps,
            "timestamp": self.timestamp,
        }

    @staticmethod
    def alert_boundary(vitals_obj: "Vitals") -> List[str]:
        """
        Very small rule-based checks — returns alert messages list.
        Extend or replace with ML-based checks as needed.
        """
        alerts = []
        if vitals_obj.hydration is not None and (vitals_obj.hydration < 20 or vitals_obj.hydration > 80):
            alerts.append(f"Hydration out of range: {vitals_obj.hydration}")
        if vitals_obj.sleep is not None and (vitals_obj.sleep < 3 or vitals_obj.sleep > 12):
            alerts.append(f"Sleep out of range: {vitals_obj.sleep}")
        if vitals_obj.hb is not None and (vitals_obj.hb < 40 or vitals_obj.hb > 140):
            alerts.append(f"Heartbeat out of range: {vitals_obj.hb}")
        if vitals_obj.bp_systolic is not None and (vitals_obj.bp_systolic < 80 or vitals_obj.bp_systolic > 200):
            alerts.append(f"BP systolic out of range: {vitals_obj.bp_systolic}")
        if vitals_obj.bp_diastolic is not None and (vitals_obj.bp_diastolic < 40 or vitals_obj.bp_diastolic > 130):
            alerts.append(f"BP diastolic out of range: {vitals_obj.bp_diastolic}")
        if vitals_obj.steps is not None and vitals_obj.steps < 0:
            alerts.append(f"Steps negative: {vitals_obj.steps}")
        return alerts


def clear_matrices():
    """Clear the in-memory matrices (useful for reloading or tests)."""
    for l in VitalsMatrix:
        l.clear()
    TimeStamps.clear()


def _insert_log(db: Session, user_id: Optional[int], action: str):
    """
    Try to persist an alert to logs table.
    This function will attempt to use crud.create_log if available,
    otherwise do a direct insert using models.Log if models exist.
    """
    if db is None:
        return
    try:
        if crud and hasattr(crud, "create_log"):
            crud.create_log(db, user_id, action)
            return
    except Exception:
        pass

    # fallback direct insert if models.Log available
    try:
        if models and hasattr(models, "Log"):
            log = models.Log(user_id=user_id, action=action, timestamp=datetime.datetime.utcnow())
            db.add(log)
            db.commit()
            return
    except Exception:
        try:
            db.rollback()
        except Exception:
            pass
    # if we cannot persist, just print (so alert isn't lost during dev)
    print("LOG (not persisted):", {"user_id": user_id, "action": action})


def load_vitals_from_db(db: Session, user_id: Optional[int] = None):
    """
    Populate VitalsMatrix and TimeStamps from DB records.
    If user_id is provided, load for that user only. Otherwise load all vitals (ordered by timestamp).
    NOTE: This clears existing matrices first.
    """
    clear_matrices()
    if db is None:
        return

    # try to use crud.get_vitals_for_user
    records = None
    try:
        if user_id is not None and crud and hasattr(crud, "get_vitals_for_user"):
            records = crud.get_vitals_for_user(db, user_id)
        elif crud and hasattr(crud, "get_all_vitals") :
            # optional helper
            records = crud.get_all_vitals(db)
    except Exception:
        records = None

    # fallback to direct model query
    if records is None:
        try:
            if models and hasattr(models, "Vitals"):
                records = db.query(models.Vitals).order_by(models.Vitals.timestamp).all()
            else:
                records = []
        except Exception:
            records = []

    # instantiate Vitals objects (which append to matrices)
    for rec in records:
        try:
            temp = Vitals(
                hydration=getattr(rec, "hydration", None),
                sleep=getattr(rec, "sleep", None),
                hb=getattr(rec, "heartbeat", None),
                bp_systolic=getattr(rec, "bp_systolic", None),
                bp_diastolic=getattr(rec, "bp_diastolic", None),
                steps=getattr(rec, "steps", None),
                timestamp=getattr(rec, "timestamp", None),
            )
            alerts = Vitals.alert_boundary(temp)
            if alerts:
                for a in alerts:
                    _insert_log(db, getattr(rec, "user_id", None), f"Vitals alert: {a}")
        except Exception as ex:
            # do not fail loading due to one bad record
            print("Skipping record during load_vitals_from_db:", ex)


def add_vitals_record(
    db: Session, user_id: int,
    hydration: Optional[float] = None,
    sleep: Optional[float] = None,
    heartbeat: Optional[float] = None,
    bp_systolic: Optional[float] = None,
    bp_diastolic: Optional[float] = None,
    steps: Optional[int] = None,
    timestamp: Optional[datetime.datetime] = None
) -> Any:
    """
    Create a vitals DB record (via crud if available), add to in-memory matrices,
    run alerts and log them. Returns the DB record if successful, otherwise None.
    """
    db_record = None
    timestamp = timestamp or datetime.datetime.utcnow()

    # Try using crud.create_vitals / add_vitals if available
    try:
        if crud:
            # common names: create_vitals(db, user_id, vitals_in) or add_vitals(db, user_id, vitals_dict)
            if hasattr(crud, "create_vitals"):
                from types import SimpleNamespace
                vit_in = SimpleNamespace(hydration=hydration, sleep=sleep, heartbeat=heartbeat,
                                         bp_systolic=bp_systolic, bp_diastolic=bp_diastolic,
                                         steps=steps, timestamp=timestamp)
                db_record = crud.create_vitals(db, user_id, vit_in)
            elif hasattr(crud, "add_vitals"):
                db_record = crud.add_vitals(db, user_id, type("X", (), {"dict": lambda self=None: {
                    "hydration": hydration, "sleep": sleep, "heartbeat": heartbeat,
                    "bp_systolic": bp_systolic, "bp_diastolic": bp_diastolic, "steps": steps,
                    "timestamp": timestamp
                }})())
    except Exception:
        db_record = None

    # fallback: direct model insert
    if db_record is None:
        try:
            if models and hasattr(models, "Vitals"):
                v = models.Vitals(
                    user_id=user_id,
                    hydration=hydration,
                    sleep=sleep,
                    heartbeat=heartbeat,
                    bp_systolic=bp_systolic,
                    bp_diastolic=bp_diastolic,
                    steps=steps,
                    timestamp=timestamp
                )
                db.add(v)
                db.commit()
                db.refresh(v)
                db_record = v
        except Exception:
            try:
                db.rollback()
            except Exception:
                pass
            db_record = None

    # always update in-memory matrices (create a Vitals instance)
    try:
        temp = Vitals(
            hydration=hydration,
            sleep=sleep,
            hb=heartbeat,
            bp_systolic=bp_systolic,
            bp_diastolic=bp_diastolic,
            steps=steps,
            timestamp=timestamp
        )
    except Exception as ex:
        print("Failed to append vitals to in-memory matrix:", ex)
        temp = None

    # run alerts & persist logs
    if temp:
        alerts = Vitals.alert_boundary(temp)
        for a in alerts:
            _insert_log(db, user_id, f"Vitals alert: {a}")

    return db_record
