import unittest
from graph.Vertex import Vertex

class TestVertexMethods(unittest.TestCase):
  def setUp(self):
    self.vertex = Vertex("WETH")

  def test_vertex_has_value(self):
    assert self.vertex.value is not None

  def tearDown(self):
    return super().tearDown()


if __name__ == "__main__":
  unittest.main()