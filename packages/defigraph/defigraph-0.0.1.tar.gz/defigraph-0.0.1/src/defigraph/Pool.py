class Pool:
  def __init__(self, address, chainId, token0, token1, liquidity):
    self.address = address
    self.chainId = chainId
    self.token0 = token0
    self.token1 = token1
    self.liquidity = liquidity