import sqlite3
import json
from datetime import datetime

# This file manages all database operations for the assistant's long-term memory.

DB_FILE = "vedic_memory.db"

def init_db(logger=print):
    """
    Initializes the database and creates the necessary tables if they don't exist.
    """
    try:
        con = sqlite3.connect(DB_FILE)
        cur = con.cursor()

        # Create the events table
        # Using a TEXT column to store JSON details for flexibility.
        cur.execute("""
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY,
                timestamp TEXT NOT NULL,
                event_type TEXT NOT NULL,
                details_json TEXT
            )
        """)

        con.commit()
        con.close()
        logger(f"[Database] Database '{DB_FILE}' initialized successfully.")
    except Exception as e:
        logger(f"[Database] Error during initialization: {e}")

def add_event(event_type: str, details: dict, logger=print):
    """
    Adds a new event to the database.

    Args:
        event_type: A string describing the type of event (e.g., 'command_executed', 'preference_set').
        details: A dictionary containing the details of the event.
        logger: The function to use for logging.
    """
    try:
        con = sqlite3.connect(DB_FILE)
        cur = con.cursor()

        timestamp = datetime.now().isoformat()
        details_str = json.dumps(details)

        cur.execute(
            "INSERT INTO events (timestamp, event_type, details_json) VALUES (?, ?, ?)",
            (timestamp, event_type, details_str)
        )

        con.commit()
        con.close()
        logger(f"[Database] Logged event '{event_type}' successfully.")
        return True
    except Exception as e:
        logger(f"[Database] Error adding event: {e}")
        return False

def get_last_event_by_type(event_type: str, logger=print):
    """
    Retrieves the most recent event of a specific type.

    Args:
        event_type: The type of event to search for.
        logger: The function to use for logging.

    Returns:
        A dictionary representing the event, or None if not found.
    """
    try:
        con = sqlite3.connect(DB_FILE)
        # Return rows as dictionaries instead of tuples
        con.row_factory = sqlite3.Row
        cur = con.cursor()

        cur.execute(
            "SELECT * FROM events WHERE event_type = ? ORDER BY timestamp DESC LIMIT 1",
            (event_type,)
        )

        row = cur.fetchone()
        con.close()

        if row:
            logger(f"[Database] Found last event of type '{event_type}'.")
            # Convert the row object to a standard dictionary
            event = dict(row)
            # Parse the JSON string back into a dictionary
            event['details_json'] = json.loads(event['details_json'])
            return event
        else:
            logger(f"[Database] No event of type '{event_type}' found.")
            return None

    except Exception as e:
        logger(f"[Database] Error getting event: {e}")
        return None

# Example of initializing the DB when the module is run
if __name__ == "__main__":
    print("Initializing the Vedic Memory database...")
    init_db()
    print("Adding a test event...")
    add_event("test_run", {"info": "Database module was run directly."})
    print("Retrieving the test event...")
    event = get_last_event_by_type("test_run")
    if event:
        print("Retrieved Event:", event)
    print("Database test complete.")
