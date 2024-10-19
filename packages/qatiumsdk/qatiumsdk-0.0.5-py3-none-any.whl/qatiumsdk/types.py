from typing import TypedDict, Union
from .assets.base import ElementType

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

class ElementIdentifier(TypedDict):
  id: ElementId
  type: ElementType
