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


def get_pending_scheduled_tasks(logger=print):
    """
    Retrieves all scheduled tasks that are currently pending.
    """
    try:
        con = sqlite3.connect(DB_FILE)
        con.row_factory = sqlite3.Row
        cur = con.cursor()

        cur.execute(
            "SELECT * FROM events WHERE event_type = 'scheduled_task' AND json_extract(details_json, '$.status') = 'pending'"
        )

        rows = cur.fetchall()
        con.close()

        if rows:
            logger(f"[Database] Found {len(rows)} pending scheduled tasks.")
            # Convert row objects to standard dictionaries
            tasks = []
            for row in rows:
                task = dict(row)
                task['details_json'] = json.loads(task['details_json'])
                tasks.append(task)
            return tasks
        else:
            return []

    except Exception as e:
        logger(f"[Database] Error getting pending tasks: {e}")
        return []

def update_task_status(task_id: int, new_status: str, logger=print):
    """
    Updates the status of a specific scheduled task.
    """
    try:
        con = sqlite3.connect(DB_FILE)
        cur = con.cursor()

        # First, get the current details
        cur.execute("SELECT details_json FROM events WHERE id = ?", (task_id,))
        row = cur.fetchone()
        if not row:
            logger(f"[Database] Error: Could not find task with id {task_id} to update.")
            return False

        details = json.loads(row[0])
        details['status'] = new_status # Update the status
        details_str = json.dumps(details)

        cur.execute(
            "UPDATE events SET details_json = ? WHERE id = ?",
            (details_str, task_id)
        )

        con.commit()
        con.close()
        logger(f"[Database] Updated task {task_id} status to '{new_status}'.")
        return True
    except Exception as e:
        logger(f"[Database] Error updating task status: {e}")
        return False
