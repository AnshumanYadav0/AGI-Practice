from typing import Callable
from .shell_tools import RunBashCommandTool

class OpenWindowsAppTool:
    """A tool to find and open installed applications on Windows."""
    name = "open_windows_app"
    description = (
        "Finds and launches an application on Windows by its name. "
        "Use this to open programs like 'Brave', 'AutoCAD', 'QGIS', 'terminal', etc. "
        "The `app_name` should be the common name of the application."
    )

    def __init__(self, logger: Callable = print, bash_tool: RunBashCommandTool = None):
        self.logger = logger
        self.bash_tool = bash_tool

    def use(self, app_name: str):
        self.logger(f"--- Windows Tool: Attempting to open application '{app_name}' ---")

        if not self.bash_tool:
            self.logger("ERROR: The bash tool was not provided to the Windows App Launcher tool.")
            return "Sorry, the app launcher tool is not properly configured."

        # Sanitize app_name for PowerShell
        safe_app_name = app_name.replace("'", "''")

        # PowerShell command to find and launch the app, and output a success marker.
        # If the app is not found, `Get-StartApps` returns nothing, so the ForEach-Object block is not executed.
        command = (
            f'powershell -Command "$app = Get-StartApps -Name \'*{safe_app_name}*\' | Select-Object -First 1; '
            f'if ($app) {{ Start-Process -FilePath $app.AppID; Write-Output \'LAUNCH_SUCCESS\' }} else {{ Write-Output \'APP_NOT_FOUND\' }}"'
        )

        self.logger(f"Executing PowerShell command via bash tool: {command}")

        result = self.bash_tool.use(command=command)
        self.logger(f"Bash tool returned: '{result}'") # Add extra logging for debugging

        # Check for the success marker in the output.
        if "LAUNCH_SUCCESS" in result:
            success_msg = f"Successfully launched the application '{app_name}'."
            self.logger(success_msg)
            return success_msg
        elif "APP_NOT_FOUND" in result:
            error_msg = f"Sorry, I could not find an installed application named '{app_name}'. Please check the name."
            self.logger(f"Failed to find '{app_name}'.")
            return error_msg
        else:
            error_msg = f"An unknown error occurred while trying to launch '{app_name}'. Details: {result}"
            self.logger(error_msg)
            return error_msg
