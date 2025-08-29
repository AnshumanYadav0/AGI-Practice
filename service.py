import time
from assistant import Assistant
import database

class VedicService:
    """
    Represents the assistant running as a continuous, long-running service.
    This enables proactive behaviors and monitoring.
    """
    def __init__(self):
        print("Initializing Vedic Service...")
        # In a real service, you would pass the real tools here.
        self.assistant = Assistant()
        # Ensure the database is ready.
        database.init_db()
        self.is_running = False

    def perform_proactive_check(self):
        """
        This method is called periodically by the service loop.
        It's the entry point for all proactive (non-command-driven) behaviors.
        """
        # In a real application, this could trigger multiple checks.
        # For example, check the calendar, check system health, check for news, etc.

        # Example: A simple proactive check.
        # Let's imagine a tool that checks the time.
        from datetime import datetime
        now = datetime.now()
        if now.minute == 0: # Run on the hour
            self.assistant.logger("--- [Proactive Check] ---")
            self.assistant.logger(f"It's {now.hour}:00. Time for an hourly check.")
            # Here, the assistant could use a tool to check for reminders in its memory.
            # e.g., self.assistant.execute_command("recall reminders for this hour")

    def start(self):
        """Starts the main service loop."""
        self.is_running = True
        print("Vedic Service started. Running in a loop (press Ctrl+C to stop).")

        while self.is_running:
            try:
                # 1. Perform proactive checks.
                self.perform_proactive_check()

                # 2. Listen for incoming commands.
                # In a real service, this would not be a sleep. It would be a non-blocking
                # listener, e.g., a socket server, a message queue consumer (like RabbitMQ),
                # or a file-based queue that the GUI writes to.
                # For this simulation, we just sleep to represent the service being idle
                # but ready to be interrupted by a command.

                time.sleep(60) # Check once per minute

            except KeyboardInterrupt:
                print("\nShutdown signal received.")
                self.stop()
            except Exception as e:
                print(f"An error occurred in the service loop: {e}")
                time.sleep(60) # Wait before retrying after an error

    def stop(self):
        """Stops the service loop."""
        print("Vedic Service stopping.")
        self.is_running = False

if __name__ == "__main__":
    service = VedicService()
    # In a real deployment, this would be managed by a service manager like systemd.
    service.start()
