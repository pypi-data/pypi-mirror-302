import pyvista as pv
import trimesh
import numpy as np
from .mesh_exceptions import MeshSDFError, MeshVisualizationError
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from skimage import measure

def visualize_mesh(mesh: trimesh.Trimesh, logger, show_edges=True, show_normals=False, cmap="viridis", title="Mesh Visualization"):
    logger.info(f"Preparing mesh visualization: {title}")

    try:
        # Convert trimesh to pyvista PolyData
        vertices = mesh.vertices
        faces = np.column_stack((np.full(len(mesh.faces), 3), mesh.faces)).flatten()
        pv_mesh = pv.PolyData(vertices, faces)

        # Create a plotter
        plotter = pv.Plotter()
        
        # Add the mesh to the plotter
        plotter.add_mesh(pv_mesh, show_edges=show_edges, cmap=cmap)

        # Add normals if requested
        if show_normals:
            # Calculate face centers
            face_centers = pv_mesh.cell_centers().points
            # Get face normals
            face_normals = pv_mesh.face_normals

            # Add arrows for face normals
            plotter.add_arrows(face_centers, face_normals, mag=0.1, color="red")

        # Add the title
        plotter.add_title(title)

        # Add orientation widget
        plotter.add_axes()

        logger.info(f"Displaying mesh visualization: {title}")
        plotter.show()
    except AttributeError as e:
        logger.error(f"Mesh is missing an expected attribute: {str(e)}")
        raise MeshVisualizationError(f"Failed to visualize mesh: {str(e)}") from e
    except ValueError as e:
        logger.error(f"Invalid value encountered during visualization: {str(e)}")
        raise MeshVisualizationError(f"Failed to visualize mesh: {str(e)}") from e
    except Exception as e:
        logger.error(f"Unexpected error during mesh visualization: {str(e)}")
        raise MeshVisualizationError(f"Failed to visualize mesh: {str(e)}") from e

def visualize_sdf(sdf: np.ndarray, logger, title="SDF Visualization"):
    """
    Visualize a 2D slice of the 3D SDF.
    
    Args:
    sdf (np.ndarray): The 3D SDF array.
    logger: The logger object.
    """
    logger.info(f"Visualizing SDF slice: {title}")
    
    try:
        # Take a middle slice of the 3D SDF
        middle_slice = sdf[:, :, sdf.shape[2]//2]
        
        plt.figure(figsize=(10, 8))
        plt.imshow(middle_slice, cmap='RdBu', interpolation='nearest')
        plt.colorbar(label='Signed Distance')
        plt.title(title)
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.show()
        
        logger.info("SDF visualization completed")
    
    except Exception as e:
        logger.error(f"Error during SDF visualization: {str(e)}")
        raise MeshSDFError(f"Failed to visualize SDF: {str(e)}") from e
    
def visualize_curvature(mesh: trimesh.Trimesh, curvatures: np.ndarray, logger, title="Curvature Visualization"):
    logger.info(f"Preparing curvature visualization: {title}")

    try:
        # Convert trimesh to pyvista PolyData
        vertices = mesh.vertices
        faces = np.column_stack((np.full(len(mesh.faces), 3), mesh.faces)).flatten()
        pv_mesh = pv.PolyData(vertices, faces)

        # Add curvature data to the mesh
        pv_mesh.point_data["Curvature"] = curvatures

        # Create a plotter
        plotter = pv.Plotter()
        
        # Add the mesh to the plotter, coloring by curvature
        plotter.add_mesh(pv_mesh, scalars="Curvature", cmap="coolwarm", show_edges=False)

        # Add a color bar
        plotter.add_scalar_bar("Curvature")

        # Add a title
        plotter.add_title(title)

        # Add orientation widget
        plotter.add_axes()

        logger.info("Displaying curvature visualization")
        plotter.show()
    except AttributeError as e:
        logger.error(f"Mesh or curvature data is missing an expected attribute: {str(e)}")
        raise MeshVisualizationError(f"Failed to visualize curvature: {str(e)}") from e
    except ValueError as e:
        logger.error(f"Invalid value encountered during curvature visualization: {str(e)}")
        raise MeshVisualizationError(f"Failed to visualize curvature: {str(e)}") from e
    except Exception as e:
        logger.error(f"Unexpected error during curvature visualization: {str(e)}")
        raise MeshVisualizationError(f"Failed to visualize curvature: {str(e)}") from e

def visualize_sdf_3d(sdf, logger, title="SDF Visualization", iso_value=0):
    """
    Visualize the Signed Distance Function (SDF) in 3D using an isosurface.
    
    Args:
    sdf (np.ndarray): 3D numpy array representing the SDF.
    logger: The logger object.
    title (str): Title for the visualization.
    iso_value (float): The isosurface value to visualize.
    """
    logger.info(f"Visualizing SDF in 3D: {title}")
    
    try:
        # Use marching cubes to obtain the surface mesh of the SDF
        verts, faces, normals, values = measure.marching_cubes(sdf, iso_value)

        # Create a new 3D figure
        fig = plt.figure(figsize=(10, 10))
        ax = fig.add_subplot(111, projection='3d')

        # Plot the surface
        mesh = ax.plot_trisurf(verts[:, 0], verts[:, 1], faces, verts[:, 2],
                               cmap='viridis', lw=1)

        # Customize the visualization
        ax.set_title(title)
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')

        # Add a color bar
        fig.colorbar(mesh, ax=ax, shrink=0.5, aspect=5)

        # Show the plot
        plt.show()

    except Exception as e:
        logger.error(f"Failed to visualize SDF in 3D: {str(e)}")
        raise MeshVisualizationError(f"SDF 3D visualization failed: {str(e)}") from e
