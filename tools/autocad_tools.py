# This file contains tools for interacting with Autodesk AutoCAD.

# --- DUMMY AutoCAD API ---
# This section simulates the pyautocad library for environments where it's not installed.
try:
    from pyautocad import Autocad, APoint
except ImportError:
    # print("WARNING: pyautocad library not found. This script is for demonstration purposes only.")
    class _DummyModel:
        def AddBox(self, point1, width, height, depth):
            # print(f"DUMMY MODE: Drawing a box from {point1} with width {width}, height {height}, depth {depth}")
            return "DummyBox"
    class Autocad:
        def __init__(self, *args, **kwargs):
            self.doc = self
            self.Name = "Dummy AutoCAD"
            self.model = _DummyModel()
        def prompt(self, msg):
            # print(f"DUMMY PROMPT: {msg.strip()}")
            pass
    class APoint:
        def __init__(self, x, y):
            self.x = x
            self.y = y
        def __str__(self):
            return f"APoint({self.x}, {self.y})"
# --- End of Dummy API ---


class CreateRectangleTool:
    """A tool to create a rectangle in AutoCAD."""
    name = "create_autocad_rectangle"
    description = "Creates a 2D rectangle in a running AutoCAD application. Requires specifying `width` and `height`. The starting point is assumed to be (0,0)."

    def __init__(self, logger=print):
        self.logger = logger

    def use(self, width: int, height: int, point1: tuple = (0, 0)):
        self.logger(f"--- AutoCAD Tool: Attempting to create rectangle ---")
        self.logger(f"Parameters: start_point={point1}, width={width}, height={height}")

        try:
            acad = Autocad(create_if_not_exists=True)
            acad.prompt("Connected to AutoCAD from Python\n")
            self.logger(f"Successfully connected to AutoCAD version: {acad.doc.Name}")

            p1 = APoint(point1[0], point1[1])
            acad.model.AddBox(p1, width, height, 0)

            self.logger("Rectangle created successfully in AutoCAD.")
            return "Rectangle created successfully."
        except Exception as e:
            error_message = f"Failed to control AutoCAD. Please ensure AutoCAD is running and accessible. Error: {e}"
            self.logger(error_message)
            return error_message


class AddCircleTool:
    """A dummy tool to add a circle in AutoCAD."""
    name = "add_autocad_circle"
    description = "Draws a circle in AutoCAD. Requires specifying the center point (`center_x`, `center_y`) and the `radius`. (Currently a dummy tool)."

    def __init__(self, logger=print):
        self.logger = logger

    def use(self, center_x: int, center_y: int, radius: int):
        self.logger("--- AutoCAD Tool: Attempting to add circle (Dummy) ---")
        self.logger(f"Parameters: center=({center_x},{center_y}), radius={radius}")
        return f"DUMMY: Circle with radius {radius} added in AutoCAD."
