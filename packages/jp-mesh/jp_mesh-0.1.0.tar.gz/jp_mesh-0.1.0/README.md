# Mesh Processing Tools

A Python package for 3D mesh processing and analysis, offering a suite of tools for loading, analyzing, simplifying, and computing properties of 3D meshes.

## Features

- Mesh loading and analysis
- Mesh simplification
- Curvature calculation
- Signed Distance Field (SDF) computation
- Comprehensive error handling

## Installation

You can install Mesh Processing Tools using pip:

```bash
pip install jp-mesh-processing
```

## Quick Start

To use the package, you can import the necessary functions and classes from the `mesh_processing` module.

```python
from jp_mesh_processing import load_mesh, analyze_mesh, simplify_mesh, calculate_mesh_curvature, compute_sdf_mesh_to_sdf

# Example usage
mesh = load_mesh("path/to/your/mesh.obj")
analysis = analyze_mesh(mesh)
simplified_mesh = simplify_mesh(mesh, 0.5)
curvatures = calculate_mesh_curvature(mesh)
sdf = compute_sdf_mesh_to_sdf(mesh, 64)
```

## TODO

- [ ] Implement better testing for SDF computation with various parameter inputs
- [ ] Replace 'skull.obj' with a licensed 3D model from custom assets.jeevanpillay.com
- [ ] Integrate documentation and visualization into a web application:
  - [ ] Set up apps/www website for project documentation
  - [ ] Develop web-based visualization for mesh and SDF converted files
  - [ ] Ensure fast and easy access to visualizations and documentation
- [ ] Review and update dependencies:
  - [ ] Remove unused dependencies from requirements.txt and setup files
  - [ ] Verify the necessity of 'rtree' and remove if unused
  - [ ] Ensure 'pymeshlab' and 'pyvista' are properly utilized in the codebase
- [ ] Pylint & Pytest Integration

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
