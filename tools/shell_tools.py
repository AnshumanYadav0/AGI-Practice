from typing import Callable

class RunBashCommandTool:
    """A powerful tool to execute shell commands."""
    name = "run_bash_command"
    description = (
        "Executes a single, valid shell command in the bash terminal. "
        "Use this for general system operations, file manipulation, running programs, and installing packages. "
        "This tool is powerful and can modify the system, so use it with caution."
    )

    def __init__(self, logger: Callable = print, run_in_bash_session_tool: Callable = None):
        self.logger = logger
        self.run_in_bash_session_tool = run_in_bash_session_tool

    def use(self, command: str):
        self.logger(f"--- Shell Tool: Executing command: '{command}' ---")

        if not self.run_in_bash_session_tool:
            self.logger("ERROR: The bash execution tool was not provided.")
            return "Sorry, the shell tool is not available."

        # SECURITY NOTE: In a real-world application, this is a critical point for security.
        # You would want to add checks here:
        # 1. Sanitize the command to prevent injection attacks.
        # 2. Use a whitelist of allowed commands.
        # 3. Ask the user for confirmation before executing potentially destructive commands (e.g., 'rm', 'sudo').
        # For this simulation, we execute the command directly.

        try:
            # The provided tool function is called here.
            result = self.run_in_bash_session_tool(command)
            self.logger("Command executed successfully.")
            # It's good practice to return the output to the agent.
            return f"Successfully executed command '{command}'.\nOutput:\n{result}"
        except Exception as e:
            error_message = f"An error occurred while executing the shell command: {e}"
            self.logger(error_message)
            return error_message


class TroubleshootDevIssueTool:
    """A high-level tool to troubleshoot and fix common development environment issues."""
    name = "troubleshoot_dev_issue"
    description = (
        "A high-level tool that attempts to automatically diagnose and fix a development environment problem. "
        "Use this when a user reports an issue like 'TensorFlow is not installing'. "
        "The `issue_description` should be the user's full report of the problem."
    )

    def __init__(self, logger: Callable = print, bash_tool: RunBashCommandTool = None):
        self.logger = logger
        self.bash_tool = bash_tool

    def use(self, issue_description: str):
        self.logger(f"--- Fix-It Tool: Troubleshooting issue: '{issue_description}' ---")

        if not self.bash_tool:
            self.logger("ERROR: The bash tool was not provided to the Fix-It tool.")
            return "Sorry, the troubleshooting tool is not properly configured."

        # Simulate a workflow for a specific issue. An LLM could generate this workflow dynamically.
        if "tensorflow" in issue_description.lower():
            self.logger("Issue appears to be related to TensorFlow. Starting troubleshooting workflow...")

            # Step 1: Attempt a clean installation
            self.logger("Step 1: Attempting to install TensorFlow via pip.")
            install_command = "pip install tensorflow"
            install_result = self.bash_tool.use(command=install_command)
            self.logger(install_result)

            # Step 2: Verify the installation
            self.logger("Step 2: Verifying installation by trying to import TensorFlow.")
            verify_command = "python -c \"import tensorflow as tf; print(f'TensorFlow version {tf.__version__} installed.')\""
            verify_result = self.bash_tool.use(command=verify_command)
            self.logger(verify_result)

            if "version" in verify_result.lower():
                return "Successfully installed and verified TensorFlow. The issue should be resolved."
            else:
                return "Attempted to install TensorFlow, but verification failed. The issue might be more complex."

        return f"I'm not yet equipped to handle the issue: '{issue_description}'. I can only troubleshoot TensorFlow installation issues right now."
