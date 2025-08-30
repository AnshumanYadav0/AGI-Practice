from typing import Callable
import json

class ScreenReaderTool:
    """A tool to 'read' the current content of the screen."""
    name = "read_current_screen"
    description = (
        "Simulates taking a screenshot and using OCR to extract all visible text. "
        "Use this to get context of what the user is currently doing."
    )

    def __init__(self, logger: Callable = print):
        self.logger = logger

    def use(self):
        self.logger("--- Vision Tool: Reading screen (Simulation) ---")

        # In a real application, this would use a library like Pillow or pyautogui
        # to take a screenshot, and an OCR engine like Tesseract to extract text.
        # For this simulation, we return a hardcoded string that represents
        # a user having just opened a terminal and navigated to a project.
        simulated_screen_text = (
            "Windows PowerShell\n"
            "Copyright (C) Microsoft Corporation. All rights reserved.\n\n"
            "PS C:\\Users\\anshu> cd C:\\Users\\anshu\\projects\\my_project\n"
            "PS C:\\Users\\anshu\\projects\\my_project> code .\n"
            "PS C:\\Users\\anshu\\projects\\my_project> "
        )
        self.logger("Screen content has been read.")
        return simulated_screen_text


class WorkflowLearningTool:
    """A tool to learn a new workflow from observed screen text."""
    name = "learn_new_workflow_from_screen"
    description = (
        "Analyzes a block of text (presumably from the screen reader tool) to identify "
        "a sequence of actions. If a recognizable workflow is found, it suggests a new "
        "custom command to automate it."
    )

    def __init__(self, logger: Callable = print):
        self.logger = logger

    def use(self, screen_text: str):
        self.logger("--- Vision Tool: Analyzing screen text for workflows ---")

        # This is a simulation of a much more complex learning algorithm.
        # It looks for specific keywords to identify a known workflow.
        lower_text = screen_text.lower()
        if "cd" in lower_text and "my_project" in lower_text and "code ." in lower_text:
            self.logger("Found a 'start coding' workflow.")

            # The tool doesn't write files itself. It designs the new command
            # and the script, and returns them as a structured response.
            # The Assistant is then responsible for the file I/O.
            new_command_definition = {
                "phrase": "start my coding workflow",
                "action": "run_learned_script",
                "application": "system",
                "description": "A learned workflow to open the coding project.",
                "script_path": "learned_scripts/coding_workflow.sh"
            }

            script_content = (
                "#!/bin/bash\n"
                "# This is an auto-generated script learned by Vedic AI.\n"
                "echo 'Starting your coding workflow...'\n"
                "cd C:/Users/anshu/projects/my_project\n"
                "code .\n"
                "echo 'Workflow complete.'\n"
            )

            response = {
                "status": "workflow_found",
                "new_command": new_command_definition,
                "script_content": script_content
            }

            return json.dumps(response)

        else:
            self.logger("No recognizable workflow found in the text.")
            return json.dumps({"status": "no_workflow_found"})
