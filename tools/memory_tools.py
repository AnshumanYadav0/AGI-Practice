from typing import Callable, Dict, Any
import database

class LogEventTool:
    """A tool to save information to the assistant's long-term memory."""
    name = "log_event_to_memory"
    description = (
        "Saves a piece of information to the assistant's long-term memory. "
        "Use this to remember facts, user preferences, or the outcome of an action. "
        "The details should be a dictionary."
    )

    def __init__(self, logger: Callable = print):
        self.logger = logger

    def use(self, event_type: str, details: Dict[str, Any]):
        self.logger(f"--- Memory Tool: Logging event '{event_type}' ---")
        self.logger(f"Details: {details}")

        success = database.add_event(event_type, details, logger=self.logger)

        if success:
            return f"Successfully logged event '{event_type}' to memory."
        else:
            return f"Failed to log event '{event_type}' to memory."


class RecallEventTool:
    """A tool to retrieve information from the assistant's long-term memory."""
    name = "recall_last_event_from_memory"
    description = (
        "Retrieves the most recent event of a specific type from the assistant's long-term memory."
    )

    def __init__(self, logger: Callable = print):
        self.logger = logger

    def use(self, event_type: str):
        self.logger(f"--- Memory Tool: Recalling last event of type '{event_type}' ---")

        event = database.get_last_event_by_type(event_type, logger=self.logger)

        if event:
            # Format the event for a user-friendly response
            timestamp = event['timestamp']
            details = event['details_json']
            self.logger(f"Found event: {event}")
            return f"I found an event of type '{event_type}' from {timestamp}. Details: {details}"
        else:
            self.logger(f"No event of type '{event_type}' found in memory.")
            return f"I couldn't find any recent events of type '{event_type}' in my memory."
