import trimesh
import numpy as np
from .mesh_exceptions import MeshSimplificationError
import pymeshlab

def simplify_mesh(mesh: trimesh.Trimesh, target_percent: float, logger) -> trimesh.Trimesh:
    """
    Simplify the mesh to a target percentage of its original face count using fast_simplification.
    
    Args:
    mesh (trimesh.Trimesh): The input mesh to simplify.
    target_percent (float): The target percentage of faces to keep (0.0 to 1.0).
    logger: The logger object.
    
    Returns:
    trimesh.Trimesh: The simplified mesh.
    """
    logger.info(f"Starting mesh simplification. Original face count: {len(mesh.faces)}")
    
    if not 0.0 < target_percent <= 1.0:
        raise ValueError("target_percent must be between 0.0 and 1.0")
    
    try:
        # Convert trimesh to pymeshlab mesh
        ms = pymeshlab.MeshSet()
        ms.add_mesh(pymeshlab.Mesh(mesh.vertices, mesh.faces))
        
        # Calculate target face count
        target_faces = int(len(mesh.faces) * target_percent)
        
        # Simplify the mesh
        ms.meshing_decimation_quadric_edge_collapse(targetfacenum=target_faces)
        
        # Get the simplified mesh
        simplified_mesh = ms.current_mesh()
        
        # Convert back to trimesh
        simplified_trimesh = trimesh.Trimesh(vertices=simplified_mesh.vertex_matrix(), 
                                             faces=simplified_mesh.face_matrix())
        
        logger.info(f"Mesh simplification completed. New face count: {len(simplified_trimesh.faces)}")
        logger.info(f"Reduction: {(1 - len(simplified_trimesh.faces) / len(mesh.faces)) * 100:.2f}%")
        
        return simplified_trimesh
    
    except Exception as e:
        logger.error(f"Error during mesh simplification: {str(e)}")
        raise MeshSimplificationError(f"Failed to simplify mesh: {str(e)}") from e

def analyze_simplification(original_mesh: trimesh.Trimesh, simplified_mesh: trimesh.Trimesh, logger) -> dict:
    """
    Analyze the differences between the original and simplified meshes.
    
    Args:
    original_mesh (trimesh.Trimesh): The original mesh.
    simplified_mesh (trimesh.Trimesh): The simplified mesh.
    logger: The logger object.
    
    Returns:
    dict: A dictionary containing analysis results.
    """
    logger.info("Analyzing simplification results")
    
    try:
        analysis = {
            "original_vertices": len(original_mesh.vertices),
            "original_faces": len(original_mesh.faces),
            "simplified_vertices": len(simplified_mesh.vertices),
            "simplified_faces": len(simplified_mesh.faces),
            "vertex_reduction": (1 - len(simplified_mesh.vertices) / len(original_mesh.vertices)) * 100,
            "face_reduction": (1 - len(simplified_mesh.faces) / len(original_mesh.faces)) * 100,
            "original_volume": original_mesh.volume,
            "simplified_volume": simplified_mesh.volume,
            "volume_difference": abs(original_mesh.volume - simplified_mesh.volume) / original_mesh.volume * 100,
            "original_area": original_mesh.area,
            "simplified_area": simplified_mesh.area,
            "area_difference": abs(original_mesh.area - simplified_mesh.area) / original_mesh.area * 100,
        }
        
        logger.info("Simplification analysis completed")
        return analysis
    
    except Exception as e:
        logger.error(f"Error during simplification analysis: {str(e)}")
        raise MeshSimplificationError(f"Failed to analyze simplification: {str(e)}") from e
