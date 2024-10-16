from typing import Optional, Union
from defigraph.Pool import Pool

class Vertex:
  def __init__(self, name: Optional[Union[str,int]], pool: Pool, decimals: int):
    self.name = name
    self.pool = pool
    self.decimals = decimals

  def __repr__(self):
    return f"{self.name}"
  
  