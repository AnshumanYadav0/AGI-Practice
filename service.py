import time
import os
import json
from assistant import Assistant
import database
from datetime import datetime, timedelta
import re

COMMAND_QUEUE_FILE = "command_queue.txt"

class VedicService:
    """
    Represents the assistant running as a continuous, long-running service.
    This enables proactive behaviors and monitoring.
    """
    def __init__(self):
        print("Initializing Vedic Service...")
        self.assistant = Assistant()
        database.init_db()
        self.is_running = False
        if os.path.exists(COMMAND_QUEUE_FILE):
            os.remove(COMMAND_QUEUE_FILE)

    def check_for_commands(self):
        """Checks the command queue file for a new command from a client."""
        if os.path.exists(COMMAND_QUEUE_FILE):
            with open(COMMAND_QUEUE_FILE, 'r') as f:
                command = f.read().strip()
            os.remove(COMMAND_QUEUE_FILE)
            if command:
                self.assistant.logger(f"[Service] Received command '{command}' from queue.")
                self.assistant.execute_command(command)

    def _is_task_due(self, task):
        """
        Parses a task's time_string and timestamp to see if it's due.
        This is a simple simulation and only understands "in X minutes".
        """
        time_string = task['details_json'].get('time_string', '').lower()

        # Simple case: "in X minutes"
        match = re.search(r'in (\d+) minute', time_string)
        if match:
            minutes_to_wait = int(match.group(1))
            scheduled_time = datetime.fromisoformat(task['timestamp'])
            due_time = scheduled_time + timedelta(minutes=minutes_to_wait)
            return datetime.now() >= due_time

        # Default case for this simulation: assume any other time string means "now"
        return True

    def perform_proactive_check(self):
        """
        Checks the database for pending scheduled tasks and executes them if they are due.
        """
        pending_tasks = database.get_pending_scheduled_tasks(logger=self.assistant.logger)

        for task in pending_tasks:
            if self._is_task_due(task):
                self.assistant.logger(f"--- [Proactive Task] ---")
                self.assistant.logger(f"Executing scheduled task #{task['id']}: {task['details_json']['task']}")

                # The assistant gives itself the command to execute the task.
                self.assistant.execute_command(task['details_json']['task'])

                # Mark the task as complete so it doesn't run again.
                database.update_task_status(task['id'], 'complete', logger=self.assistant.logger)

    def start(self):
        """Starts the main service loop."""
        self.is_running = True
        self.assistant.logger("Vedic Service started. Running in a loop (press Ctrl+C to stop).")

        while self.is_running:
            try:
                self.check_for_commands()
                self.perform_proactive_check()
                time.sleep(5)
            except KeyboardInterrupt:
                self.stop()
            except Exception as e:
                self.assistant.logger(f"An error occurred in the service loop: {e}")
                time.sleep(20)

    def stop(self):
        """Stops the service loop."""
        self.assistant.logger("Vedic Service stopping.")
        if os.path.exists(COMMAND_QUEUE_FILE):
            os.remove(COMMAND_QUEUE_FILE)
        self.is_running = False

if __name__ == "__main__":
    service = VedicService()
    service.start()
