from typing import TypedDict, Union, Literal

class Success(TypedDict):
  status: str  # "success"

class Failure(TypedDict):
  status: str  # "failure"
  error: Union[Exception, str]

ElementId = Union[str, str]  # AssetId and ZoneId are both strings

class Coordinate(TypedDict):
  lng: float
  lat: float

class Bounds(TypedDict):
  ne: Coordinate
  sw: Coordinate


AssetTypes = {
  "PIPE": "Pipe",
  "JUNCTION": "Junction",
  "VALVE": "Valve",
  "PUMP": "Pump",
  "SUPPLY_SOURCE": "SupplySource",
  "TANK": "Tank"
}

ElementTypes = {
  **AssetTypes,
  "ZONE": "Zone"
}

ElementTypeKeys = Literal["PIPE", "JUNCTION", "VALVE", "PUMP", "SUPPLY_SOURCE", "TANK", "ZONE"]
ElementType = Literal["Pipe", "Junction", "Valve", "Pump", "SupplySource", "Tank", "Zone"]

class ElementIdentifier(TypedDict):
  id: ElementId
  type: ElementType
