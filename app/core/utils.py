import uuid # Import the module to work with unique identifiers (UUIDs)
def generate_uuid() -> str:
    # Create a new unique ID and convert it to a string
    return str(uuid.uuid4())
