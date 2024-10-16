import trimesh
import os
from .mesh_exceptions import InvalidPathError, MeshFileNotFoundError, MeshImportError

def load_mesh(mesh_path: str, logger) -> trimesh.Trimesh:
    logger.info(f"Loading mesh from: {mesh_path}")

    # Check if the path is valid
    if not os.path.isabs(mesh_path):
        logger.error(f"Invalid path: {mesh_path}")
        raise InvalidPathError(f"Invalid path: {mesh_path}. Please provide an absolute path.")

    # Check if the file exists
    if not os.path.exists(mesh_path):
        logger.error(f"Mesh file not found: {mesh_path}")
        raise MeshFileNotFoundError(f"Mesh file not found: {mesh_path}")
    
    try:
        mesh = trimesh.load(mesh_path)
        logger.info(f"Mesh loaded successfully. Vertices: {len(mesh.vertices)}, Faces: {len(mesh.faces)}")
        return mesh
    except Exception as e:
        logger.error(f"Error loading mesh: {str(e)}")
        raise MeshImportError(f"Error loading mesh: {str(e)}") from e