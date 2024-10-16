from logging_config import setup_logger
from mesh_load import load_mesh
from mesh_analysis import analyze_mesh, compute_mesh_normals, calculate_mesh_curvature
from mesh_visualizer import visualize_mesh, visualize_curvature, visualize_sdf, visualize_sdf_3d
from mesh_simplification import simplify_mesh, analyze_simplification
from mesh_sdf import compute_sdf_mesh_to_sdf
from mesh_exceptions import MeshLoadError, MeshAnalysisError, MeshVisualizationError, MeshSimplificationError, MeshSDFError
from utils import timeit, format_log_message

# Set up logger
logger = setup_logger(__name__)

# Configuration
MESH_PATH = r"C:\Users\iv-windows\iCloudDrive\Desktop\x\3d\obj\components\skull\skull.obj"
SIMPLIFICATION_RATIO = 0.25  # Target 50% of original face count
SDF_RESOLUTION = 64  # Resolution for SDF computation

# Control flags
DO_ORIGINAL_MESH_ANALYSIS = False
DO_ORIGINAL_MESH_VISUALIZATION = False
DO_MESH_SIMPLIFICATION = True
DO_SIMPLIFIED_MESH_ANALYSIS = False
DO_SIMPLIFIED_MESH_VISUALIZATION = False
DO_CURVATURE_CALCULATION = False
DO_SDF_COMPUTATION = True
DO_SDF_VISUALIZATION = True

@timeit
def timed_compute_sdf_mesh_to_sdf(mesh, resolution, logger):
    return compute_sdf_mesh_to_sdf(mesh, resolution, logger)

def original_workflow():
    logger.info("Starting original mesh processing workflow")

    try:
        # Load mesh
        mesh = load_mesh(MESH_PATH, logger)

        # Analyze original mesh
        if DO_ORIGINAL_MESH_ANALYSIS:
            try:
                original_analysis = analyze_mesh(mesh, logger, prefix="[ORIGINAL]")
            except MeshAnalysisError as e:
                logger.error(f"Original mesh analysis failed: {str(e)}")

        # Visualize original mesh
        if DO_ORIGINAL_MESH_VISUALIZATION:
            try:
                visualize_mesh(mesh, logger, show_edges=True, show_normals=False, title="Original Mesh")
            except MeshVisualizationError as e:
                logger.error(f"Original mesh visualization failed: {str(e)}")

        # Compute and visualize curvature
        if DO_CURVATURE_CALCULATION:
            try:
                curvatures = calculate_mesh_curvature(mesh, logger)
                if DO_ORIGINAL_MESH_VISUALIZATION:
                    visualize_curvature(mesh, curvatures, logger)
            except MeshAnalysisError as e:
                logger.error(f"Curvature calculation failed: {str(e)}")

        # Simplify mesh
        if DO_MESH_SIMPLIFICATION:
            try:
                simplified_mesh = simplify_mesh(mesh, SIMPLIFICATION_RATIO, logger)
                
                if DO_SIMPLIFIED_MESH_ANALYSIS:
                    # Analyze simplified mesh
                    simplified_analysis = analyze_mesh(simplified_mesh, logger, prefix="[SIMPLIFIED]")
                    
                    # Analyze simplification
                    simplification_analysis = analyze_simplification(mesh, simplified_mesh, logger)
                    logger.info(format_log_message("[SIMPLIFICATION]", simplification_analysis))
                
                if DO_SIMPLIFIED_MESH_VISUALIZATION:
                    # Visualize simplified mesh
                    visualize_mesh(simplified_mesh, logger, show_edges=True, show_normals=False, title="Simplified Mesh")
            except MeshSimplificationError as e:
                logger.error(f"Mesh simplification failed: {str(e)}")

        # Compute SDF
        if DO_SDF_COMPUTATION:
            try:
                print("Computing SDF...")
                sdf, computation_time = timed_compute_sdf_mesh_to_sdf(simplified_mesh, SDF_RESOLUTION, logger)
                logger.info(f"SDF computed in {computation_time:.2f} seconds")
                if DO_SDF_VISUALIZATION:
                    visualize_sdf_3d(sdf, logger)
            except MeshSDFError as e:
                logger.error(f"SDF computation or visualization failed: {str(e)}")

    except MeshLoadError as e:
        logger.error(f"Failed to load mesh: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")

    logger.info("Original mesh processing workflow completed")

def main():
    logger.info("Starting mesh processing application")
    original_workflow()
    logger.info("Mesh processing application completed")

if __name__ == "__main__":
    main()
