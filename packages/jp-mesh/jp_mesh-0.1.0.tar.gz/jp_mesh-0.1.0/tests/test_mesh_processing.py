import unittest
from pathlib import Path
from src.mesh_processing import (
    setup_logger, load_mesh, analyze_mesh, visualize_mesh,
    simplify_mesh, calculate_mesh_curvature, compute_sdf_mesh_to_sdf,
    MeshLoadError, MeshAnalysisError, MeshVisualizationError,
    MeshSimplificationError, MeshSDFError, InvalidPathError
)
from src.mesh_processing.utils import timeit

class TestMeshProcessing(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.logger = setup_logger(__name__)
        cls.TEST_DIR = Path(__file__).parent.absolute()
        cls.MESH_PATH = cls.TEST_DIR / "skull.obj"
        cls.SIMPLIFICATION_RATIO = 0.25
        cls.SDF_RESOLUTION = 64

    def setUp(self):
        try:
            self.mesh = load_mesh(str(self.MESH_PATH), self.logger)
        except InvalidPathError:
            self.fail(f"Failed to load mesh. Make sure 'skull.obj' is in the tests directory: {self.TEST_DIR}")

    def test_mesh_loading(self):
        self.assertIsNotNone(self.mesh, "Mesh should be loaded successfully")

    def test_mesh_analysis(self):
        analysis = analyze_mesh(self.mesh, self.logger, prefix="[TEST]")
        self.assertIsNotNone(analysis, "Mesh analysis should not be None")
        self.assertIn("vertex_count", analysis, "Analysis should include vertex count")
        self.assertIn("face_count", analysis, "Analysis should include face count")

    def test_mesh_simplification(self):
        simplified_mesh = simplify_mesh(self.mesh, self.SIMPLIFICATION_RATIO, self.logger)
        self.assertIsNotNone(simplified_mesh, "Simplified mesh should not be None")
        self.assertLess(len(simplified_mesh.faces), len(self.mesh.faces), "Simplified mesh should have fewer faces")

    def test_curvature_calculation(self):
        curvatures = calculate_mesh_curvature(self.mesh, self.logger)
        self.assertIsNotNone(curvatures, "Curvatures should not be None")
        self.assertEqual(len(curvatures), len(self.mesh.vertices), "Should have curvature value for each vertex")

    @timeit
    def test_sdf_computation(self):
        sdf = compute_sdf_mesh_to_sdf(self.mesh, self.SDF_RESOLUTION, self.logger)
        self.assertIsNotNone(sdf, "SDF should not be None")
        self.assertEqual(sdf.shape, (self.SDF_RESOLUTION, self.SDF_RESOLUTION, self.SDF_RESOLUTION), 
                         "SDF should have correct shape")

    def test_error_handling(self):
        with self.assertRaises(InvalidPathError):
            load_mesh("non_existent_file.obj", self.logger)

if __name__ == '__main__':
    unittest.main()
