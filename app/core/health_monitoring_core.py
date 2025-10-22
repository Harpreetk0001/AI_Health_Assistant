import datetime
from typing import List, Tuple, Optional
from app import crud

# tuple of lists: hydration, sleep, hb, bp_systolic, bp_diastolic, steps
VitalsMatrix: Tuple[List, List, List, List, List, List] = ([], [], [], [], [], [])
TimeStamps: List[datetime.datetime] = []

class Vitals:
    def __init__(self, hydration: Optional[float]=None, sleep: Optional[float]=None, hb: Optional[float]=None,
                 bp_systolic: Optional[float]=None, bp_diastolic: Optional[float]=None, steps: Optional[int]=None,
                 timestamp: Optional[datetime.datetime]=None):
        self.hydration = hydration
        self.sleep = sleep
        self.hb = hb
        self.bp_systolic = bp_systolic
        self.bp_diastolic = bp_diastolic
        self.steps = steps
        self.timestamp = timestamp or datetime.datetime.utcnow()

        VitalsMatrix[0].append(self.hydration)
        VitalsMatrix[1].append(self.sleep)
        VitalsMatrix[2].append(self.hb)
        VitalsMatrix[3].append(self.bp_systolic)
        VitalsMatrix[4].append(self.bp_diastolic)
        VitalsMatrix[5].append(self.steps)
        TimeStamps.append(self.timestamp)

    @staticmethod
    def alert_boundary(v):
        alerts = []
        if v.hydration is not None and (v.hydration < 20 or v.hydration > 80):
            alerts.append(f"Hydration out of range: {v.hydration}")
        if v.sleep is not None and (v.sleep < 3 or v.sleep > 12):
            alerts.append(f"Sleep out of range: {v.sleep}")
        if v.hb is not None and (v.hb < 40 or v.hb > 140):
            alerts.append(f"Heartbeat out of range: {v.hb}")
        if v.bp_systolic is not None and (v.bp_systolic < 80 or v.bp_systolic > 200):
            alerts.append(f"BP systolic out of range: {v.bp_systolic}")
        if v.bp_diastolic is not None and (v.bp_diastolic < 40 or v.bp_diastolic > 130):
            alerts.append(f"BP diastolic out of range: {v.bp_diastolic}")
        if v.steps is not None and v.steps < 0:
            alerts.append(f"Steps negative: {v.steps}")
        return alerts

def clear_matrices():
    for lst in VitalsMatrix:
        lst.clear()
    TimeStamps.clear()

def load_vitals_from_db(db_session, user_id: int | None = None):
    """
    Load vitals from DB into in-memory matrices.
    If user_id is None loads all vitals ordered by timestamp.
    """
    clear_matrices()
    if user_id is not None:
        records = crud.get_vitals_for_user(db_session, user_id)
    else:
        # fetch all vitals
        records = db_session.query.__self__  # placeholder to show db available
        # Use SQLAlchemy models directly to fetch all vitals ordered by timestamp
        from app import models
        records = db_session.query(models.Vitals).order_by(models.Vitals.timestamp).all()

    for rec in records:
        temp = Vitals(
            hydration=rec.hydration,
            sleep=rec.sleep,
            hb=rec.heartbeat,
            bp_systolic=rec.bp_systolic,
            bp_diastolic=rec.bp_diastolic,
            steps=rec.steps,
            timestamp=rec.timestamp
        )
        alerts = Vitals.alert_boundary(temp)
        if alerts:
            # For now print; in production, persist alerts to logs table or notify
            print("Vitals ALERTS:", alerts)
