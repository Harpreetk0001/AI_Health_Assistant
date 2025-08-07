from .activity_log import router as activity_log_router
from .conversation_log import router as conversation_log_router
from .device_integration import router as device_integration_router
from .emergency_contact import router as emergency_contact_router
from .fall_event import router as fall_event_router
from .health_vital import router as health_vital_router
from .medication import router as medication_router
from .mental_health_log import router as mental_health_log_router
from .reminder_log import router as reminder_log_router
from .suggestion import router as suggestion_router
from .ui_preference import router as ui_preference_router
from .user import router as user_router

# To collect all routers for use in main.py
all_routers = [
    activity_log_router,
    conversation_log_router,
    device_integration_router,
    emergency_contact_router,
    fall_event_router,
    health_vital_router,
    medication_router,
    mental_health_log_router,
    reminder_log_router,
    suggestion_router,
    ui_preference_router,
    user_router,
]
