# This file contains dummy tools for interacting with Autodesk Revit.

class CreateWallTool:
    """A dummy tool to create a wall in a Revit project."""
    name = "create_revit_wall"
    description = "Creates a simple, straight wall in an Autodesk Revit project. Requires `length` and `height` parameters. (Currently a dummy tool)."

    def __init__(self, logger=print):
        self.logger = logger

    def use(self, length: float, height: float):
        self.logger(f"--- Revit Tool: Attempting to create wall ---")
        self.logger(f"Parameters: length={length}, height={height}")

        try:
            # In a real pyrevit script, you would use the Revit API here.
            # This is just a placeholder demonstrating the structure.
            # from Autodesk.Revit.DB import ...

            message = f"DUMMY MODE: Wall of length {length}ft and height {height}ft created in Revit."
            self.logger(message)
            return message

        except ImportError:
            msg = "DUMMY MODE: This is a placeholder. The Revit API is not available in this environment."
            self.logger(msg)
            return msg
        except Exception as e:
            error_message = f"Failed to control Revit. Error: {e}"
            self.logger(error_message)
            return error_message
