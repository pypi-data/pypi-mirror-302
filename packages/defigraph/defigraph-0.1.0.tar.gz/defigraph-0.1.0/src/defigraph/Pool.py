from defigraph.Vertex import Vertex

class Pool:
  def __init__(self, pool_address: str, token0: Vertex, token1: Vertex, fee: int, token0_price: float, token1_price: float):
    self.address = pool_address
    self.token0 = token0
    self.token1 = token1
    self.token0_price = token0_price
    self.token1_price = token1_price
    self.fee = fee

  def __repr__(self):
    return f"{(self.token0, self.token1, self.fee)}"
  
  def __eq__(self, pool):
    return self.address == pool.address and self.fee == pool.fee and (self.token0 == pool.token0 or self.token0 == pool.token1) and (self.token1 == pool.token1 or self.token1 == pool.token0)

  def __ne__(self, pool):
    return self.address != pool.address or self.fee != pool.fee
  
  def __hash__(self):
    return hash(str(self))
