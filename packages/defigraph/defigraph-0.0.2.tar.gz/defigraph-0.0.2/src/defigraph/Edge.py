from defigraph.Pool import Pool
from math import log

class Edge:
  def __init__(self, pool: Pool):
    self.pool = pool
    self.weight = -log(self.pool.token0_price)

  def __repr__(self):
    return f"({self.pool.token0}, {self.pool.token1}, {self.weight})"
  
  def __eq__(self, edge):
    return self.pool == edge.pool
  
  def __ne__(self, edge):
    return self.pool != edge.pool