class Vertex:
  def __init__(self, name: str, decimals: int, address: str):
    self.name = name
    self.decimals = decimals
    self.address = address

  def __repr__(self):
    return f"{self.name}"

  def __eq__(self, vertex):
    return self.name == vertex.name and self.decimals == vertex.decimals and self.address == vertex.address

  def __ne__(self, vertex):
    return self.name != vertex.name or self.decimals != vertex.decimals or self.address != vertex.address

  def __hash__(self):
    return hash(str(self))