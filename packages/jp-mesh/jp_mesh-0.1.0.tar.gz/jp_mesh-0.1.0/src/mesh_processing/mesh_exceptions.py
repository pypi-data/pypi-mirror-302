class MeshError(Exception):
    """Base class for exceptions in this module."""
    pass

class MeshLoadError(MeshError):
    """Exception raised for errors in the mesh loading process."""
    pass

class MeshAnalysisError(MeshError):
    """Exception raised for errors in the mesh analysis process."""
    pass

class MeshVisualizationError(MeshError):
    """Exception raised for errors in the mesh visualization process."""
    pass

class MeshSimplificationError(MeshError):
    """Exception raised for errors in the mesh simplification process."""
    pass

class MeshLoadError(Exception):
    """Base class for exceptions in this module."""
    pass

class InvalidPathError(MeshLoadError):
    """Exception raised for invalid paths."""
    pass

class MeshFileNotFoundError(MeshLoadError):
    """Exception raised when the mesh file is not found."""
    pass

class MeshImportError(MeshLoadError):
    """Exception raised when there's an error importing the mesh."""
    pass

class MeshSDFError(MeshError):
    """Exception raised for errors in the SDF computation or visualization process."""
    pass
