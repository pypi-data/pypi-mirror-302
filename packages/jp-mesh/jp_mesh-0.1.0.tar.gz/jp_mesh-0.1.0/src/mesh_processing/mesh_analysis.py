import numpy as np
import trimesh
from .mesh_exceptions import MeshAnalysisError
from .utils import format_log_message

def calculate_genus(mesh: trimesh.Trimesh) -> int:
    V = len(mesh.vertices)
    F = len(mesh.faces)
    E = len(mesh.edges)
    euler_characteristic = V - E + F
    return int((2 - euler_characteristic) / 2)

def analyze_mesh(mesh: trimesh.Trimesh, logger, prefix: str = "[MESH]") -> dict:
    logger.info(f"Starting mesh analysis for {prefix}")
    
    try:
        analysis = {
            "vertex_count": len(mesh.vertices),
            "face_count": len(mesh.faces),
            "edge_count": len(mesh.edges),
            "surface_area": mesh.area,
            "volume": mesh.volume,
            "is_watertight": mesh.is_watertight,
            "is_convex": mesh.is_convex,
            "euler_number": mesh.euler_number,
            "genus": calculate_genus(mesh),
            "bounding_box_volume": mesh.bounding_box.volume,
            "bounding_box_oriented_volume": mesh.bounding_box_oriented.volume,
        }
        
        # Calculate the aspect ratio (max dimension / min dimension)
        dimensions = mesh.bounding_box.extents
        aspect_ratio = np.max(dimensions) / np.min(dimensions)
        analysis["aspect_ratio"] = aspect_ratio

        logger.info(format_log_message(prefix, analysis))
        return analysis
    
    except Exception as e:
        logger.error(f"Error during mesh analysis: {str(e)}")
        raise MeshAnalysisError(f"Failed to analyze mesh: {str(e)}") from e

def compute_mesh_normals(mesh: trimesh.Trimesh, logger) -> np.ndarray:
    logger.info("Computing mesh normals")
    try:
        normals = mesh.face_normals
        logger.info(f"Computed {len(normals)} face normals")
        return normals
    except Exception as e:
        logger.error(f"Failed to compute mesh normals: {str(e)}")
        raise MeshAnalysisError(f"Failed to compute mesh normals: {str(e)}") from e

def calculate_mesh_curvature(mesh: trimesh.Trimesh, logger) -> np.ndarray:
    logger.info("Calculating mesh curvature")
    
    try:
        vertex_normals = mesh.vertex_normals
        adjacency = mesh.vertex_faces
        
        curvatures = np.zeros(len(mesh.vertices))
        
        for i, adj_faces in enumerate(adjacency):
            adj_faces = adj_faces[adj_faces != -1]
            
            if len(adj_faces) > 0:
                face_normals = mesh.face_normals[adj_faces]
                curvatures[i] = np.mean(np.abs(vertex_normals[i] - face_normals))
        
        logger.info("Mesh curvature calculation completed")
        return curvatures
    except Exception as e:
        logger.error(f"Failed to calculate mesh curvature: {str(e)}")
        raise MeshAnalysisError(f"Failed to calculate mesh curvature: {str(e)}") from e
