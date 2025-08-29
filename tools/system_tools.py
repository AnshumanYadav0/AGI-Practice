# This file contains tools for system-level actions.

class RunDiagnosticsTool:
    """A dummy tool to run system diagnostics."""
    name = "run_system_diagnostics"
    description = "Runs a simulated system health check to check for issues with disk space, memory, and CPU usage."

    def __init__(self, logger=print):
        self.logger = logger

    def use(self):
        self.logger("--- System Tool: Running diagnostics... ---")
        result = "System diagnostics complete. All systems nominal."
        self.logger(result)
        return result


class CheckForUpdatesTool:
    """A dummy tool to check for software updates."""
    name = "check_for_updates"
    description = "Checks for available software updates for the operating system and key applications."

    def __init__(self, logger=print):
        self.logger = logger

    def use(self):
        self.logger("--- System Tool: Checking for updates... ---")
        result = "No new updates available."
        self.logger(result)
        return result


class OptimizePerformanceTool:
    """A dummy tool to optimize system performance."""
    name = "optimize_performance"
    description = "Performs system optimization tasks like clearing temporary files and caches to improve performance."

    def __init__(self, logger=print):
        self.logger = logger

    def use(self):
        self.logger("--- System Tool: Optimizing performance... ---")
        result = "System performance has been optimized."
        self.logger(result)
        return result
