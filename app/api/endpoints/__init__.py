from .activity_log import router as activity_log_router # Import the router instance from the activity_log module and alias it for clarity
from .conversation_log import router as conversation_log_router # Import the router instance from the conversation_log module
from .device_integration import router as device_integration_router # Import the router instance from the device_integration module
from .emergency_contact import router as emergency_contact_router # Import the router instance from the emergency_contact module
from .fall_event import router as fall_event_router # Import the router instance from the fall_event module
from .health_vital import router as health_vital_router # Import the router instance from the health_vital module
from .medication import router as medication_router # Import the router instance from the medication module
from .mental_health_log import router as mental_health_log_router # Import the router instance from the mental_health_log module
from .reminder_log import router as reminder_log_router # Import the router instance from the reminder_log module
from .suggestion import router as suggestion_router # Import the router instance from the suggestion module
from .ui_preference import router as ui_preference_router # Import the router instance from the ui_preference module
from .user import router as user_router # Import the router instance from the user module
# To collect all the routers for use in main.py
all_routers = [
    activity_log_router,        # It handles logging of physical activities
    conversation_log_router,    # It handles logs of AI–user conversations
    device_integration_router,  # It handles integration with external devices like wearables
    emergency_contact_router,   # To manages user’s emergency contact information
    fall_event_router,          # To handles fall detection event logs
    health_vital_router,        # To manages health vital records like heart rate, BP etc
    medication_router,          # Manages medication schedules and records
    mental_health_log_router,   # Logs mental health status or related notes
    reminder_log_router,        # Handles scheduled reminders for the user
    suggestion_router,          # Manages AI-generated suggestions or tips
    ui_preference_router,       # Stores and retrieves user interface preferences
    user_router,                # Handles user account and profile management
]
