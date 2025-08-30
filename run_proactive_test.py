import time
from assistant import Assistant
from service import VedicService
import database

# This script provides a clean, linear test for the proactive workflow.

def run_test():
    """
    Tests the full "schedule -> wait -> proactively execute" loop.
    """

    # --- Setup ---
    # We need a logger and dummy tools for the assistant
    def logger(msg):
        print(msg)

    def dummy_bash(command):
        logger(f"--- SIMULATED BASH: '{command}' ---")
        if "diagnostics" in command:
            return "Diagnostics completed."
        return "Command executed."

    assistant = Assistant(
        logger=logger,
        run_in_bash_session_tool=dummy_bash
    )

    # --- Phase 1: User schedules a task ---
    logger("\n--- PHASE 1: User schedules a task ---")
    schedule_command = "schedule a task to run diagnostics in 0 minutes"
    assistant.execute_command(schedule_command)

    # Verify the task was added to the database
    tasks = database.get_pending_scheduled_tasks(logger=logger)
    if not tasks:
        logger("TEST FAILED: Task was not correctly saved to the database.")
        return
    logger("SUCCESS: Task was scheduled and saved to the database.")

    # --- Phase 2: The service's proactive loop runs ---
    logger("\n--- PHASE 2: Simulating the service's proactive check ---")

    # We create a service instance to test its proactive method directly.
    # It will use the same assistant instance.
    service = VedicService()
    # We can monkey-patch the assistant for the service if needed, but for now this is fine.
    # In a real app, they would share the same assistant instance.

    # Manually call the method that the service's loop would call.
    service.perform_proactive_check()

    # --- Phase 3: Verify the outcome ---
    logger("\n--- PHASE 3: Verifying the task was executed ---")

    # Check that the task is no longer pending
    tasks = database.get_pending_scheduled_tasks(logger=logger)
    if tasks:
        logger(f"TEST FAILED: Task with ID {tasks[0]['id']} was not marked as complete.")
    else:
        logger("SUCCESS: The pending task was found and marked as complete.")

if __name__ == "__main__":
    print("--- Starting Vedic 5.0 Proactive Workflow Test ---")
    run_test()
    print("\n--- Test Finished ---")
