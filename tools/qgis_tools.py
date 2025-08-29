# This file contains tools for interacting with QGIS.

# --- DUMMY QGIS API ---
try:
    from qgis.core import QgsVectorLayer, QgsField, QgsWkbTypes, QgsCoordinateReferenceSystem
    from PyQt5.QtCore import QVariant
    QGIS_AVAILABLE = True
except ImportError:
    QGIS_AVAILABLE = False
# --- End of Dummy API ---

class CreateShapefileTool:
    """A tool to create a new, empty shapefile in QGIS."""
    name = "create_qgis_shapefile"
    description = "Creates a new, empty point-feature shapefile (.shp) in the QGIS application. Requires a `layer_name` for the new file."

    def __init__(self, logger=print):
        self.logger = logger

    def use(self, layer_name: str, output_path: str = "."):
        self.logger(f"--- QGIS Tool: Attempting to create shapefile ---")
        self.logger(f"Parameters: layer_name='{layer_name}', output_path='{output_path}'")

        if not QGIS_AVAILABLE:
            dummy_message = f"DUMMY MODE: Would create a shapefile named '{layer_name}.shp' in '{output_path}'"
            self.logger(dummy_message)
            return dummy_message

        try:
            fields = [QgsField("ID", QVariant.Int)]
            shapefile_path = f"{output_path}/{layer_name}.shp"
            writer = QgsVectorLayer.create(
                shapefile_path, "utf-8", fields, QgsWkbTypes.Point,
                QgsCoordinateReferenceSystem("EPSG:4326")
            )
            if writer.isValid():
                self.logger(f"Shapefile '{shapefile_path}' created successfully.")
                return f"Shapefile '{layer_name}' created."
            else:
                raise Exception("Failed to create a valid layer writer.")
        except Exception as e:
            error_message = f"Failed to control QGIS. Error: {e}"
            self.logger(error_message)
            return error_message
