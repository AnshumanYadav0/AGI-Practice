from typing import Callable, Dict, Any
import database

class ScheduleTaskTool:
    """A tool to schedule a future task by saving it to memory."""
    name = "schedule_task"
    description = (
        "Schedules a task to be run at a future time by saving it to the assistant's long-term memory. "
        "Requires a `task_description` (what to do) and a `time_string` (when to do it, e.g., 'in 10 minutes', 'at 8pm')."
    )

    def __init__(self, logger: Callable = print):
        self.logger = logger

    def use(self, task_description: str, time_string: str):
        self.logger(f"--- Scheduling Tool: Scheduling task '{task_description}' for '{time_string}' ---")

        # The tool's job is to simply log the scheduled event to the database.
        # The service's proactive loop will be responsible for interpreting the time_string
        # and executing the task later.

        details = {
            "task": task_description,
            "time_string": time_string,
            "status": "pending" # We can use this status to track execution
        }

        success = database.add_event(
            event_type="scheduled_task",
            details=details,
            logger=self.logger
        )

        if success:
            return f"Okay, I've scheduled the task: '{task_description}' for '{time_string}'."
        else:
            return f"Sorry, I failed to schedule the task '{task_description}'."
