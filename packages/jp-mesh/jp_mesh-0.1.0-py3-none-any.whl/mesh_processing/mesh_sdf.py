import numpy as np
import trimesh
from .mesh_exceptions import MeshSDFError
from mesh_to_sdf import mesh_to_sdf, sample_sdf_near_surface

def compute_sdf_mesh_to_sdf(mesh: trimesh.Trimesh, resolution: int, logger) -> np.ndarray:
    """
    Compute the Signed Distance Function (SDF) for a given mesh using mesh_to_sdf library.
    
    Args:
    mesh (trimesh.Trimesh): The input mesh.
    resolution (int): The resolution of the 3D grid for SDF computation.
    logger: The logger object.
    
    Returns:
    np.ndarray: 3D numpy array representing the SDF.
    """
    logger.info(f"Starting SDF computation using mesh_to_sdf with resolution {resolution}")
    
    try:
        # Get mesh bounds
        bounds = mesh.bounds
        
        # Create a grid of points within the mesh bounds
        x = np.linspace(bounds[0, 0], bounds[1, 0], resolution)
        y = np.linspace(bounds[0, 1], bounds[1, 1], resolution)
        z = np.linspace(bounds[0, 2], bounds[1, 2], resolution)
        xx, yy, zz = np.meshgrid(x, y, z)
        points = np.vstack((xx.ravel(), yy.ravel(), zz.ravel())).T

        # Compute SDF
        sdf = mesh_to_sdf(mesh, points)
        # points, sdf = sample_sdf_near_surface(mesh, number_of_points=100000)
        
        # Reshape the result to a 3D grid
        sdf = sdf.reshape((resolution, resolution, resolution))
        
        logger.info("SDF computation using mesh_to_sdf completed")
        return sdf
    
    except Exception as e:
        logger.error(f"Error during SDF computation using mesh_to_sdf: {str(e)}")
        raise MeshSDFError(f"Failed to compute SDF using mesh_to_sdf: {str(e)}") from e
