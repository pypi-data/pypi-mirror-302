from defigraph.Vertex import Vertex

class Edge:
  def __init__(self, u: Vertex, v: Vertex, weight: float=None):
    self.u = u
    self.v = v
    self.weight = weight

  def __repr__(self):
    if not self.weight:
      return f"({self.u}, {self.v})"
    else:
      return f"({self.u}, {self.v}, {self.weight})"