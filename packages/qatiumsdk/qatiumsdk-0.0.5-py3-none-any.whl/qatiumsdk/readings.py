from typing import Union, List, Dict, Literal, Optional, TypedDict
from datetime import date

# AssetReading type: either an object with value and date or None (None replaces undefined in Python)
AssetReading = Optional[Dict[str, Union[float, date]]]

# Metrics and Metric type
Metrics = {
  "PRESSURE": "pressure",
  "FLOW": "flow",
  "LEVEL": "level",
  "STATUS": "status",
  "DEMAND": "demand",
  "SETTING": "setting",
  "UPSTREAM_PRESSURE": "upstreamPressure",
  "DOWNSTREAM_PRESSURE": "downstreamPressure"
}
Metric = Literal[
  "pressure", "flow", "level", "status", "demand",
  "setting", "upstreamPressure", "downstreamPressure"
]

# GetLatestReading type
GetLatestReading = Union[
  Dict[str, Union[Metric, date]],
  Optional[Dict[str, Union[float, date]]]
]

# AssetReadingsCollection type
AssetReadingsCollection = List[Dict[str, Union[date, Dict[str, Optional[float]]]]]

# AssetReadingsQueries type
class AssetReadingsQueries(TypedDict, total=False):
  latest: Optional[Dict[str, Union[date, Dict[str, Optional[float]]]]]
  forRange: Optional[List[Dict[str, Union[date, Dict[str, Optional[float]]]]]]
  forPeriod: Optional[AssetReadingsCollection]

# SignalMetric type
SignalMetric = Literal["pressure", "flow", "level", "status", "demand", "setting"]

# Reading type
class Reading(TypedDict):
  asset: str
  property: Union[SignalMetric, Literal["upstreamPressure", "downstreamPressure"]]
  value: float
  date: date
  unit: str

# ReadingSum type
class ReadingSum(TypedDict):
  date: date
  value: float
  unit: str

# ReadingOption type: A union of Reading, Reading[], ReadingSum, ReadingSum[]
ReadingOption = Union[
  Reading,
  List[Reading],
  ReadingSum,
  List[ReadingSum]
]

# AssetReadingsByType type
class AssetReadingsByType(TypedDict):
  flow: Optional[ReadingOption]
  pressure: Optional[ReadingOption]
  demand: Optional[ReadingOption]
  level: Optional[ReadingOption]
  setting: Optional[ReadingOption]
  status: Optional[ReadingOption]
  upstreamPressure: Optional[ReadingOption]
  downstreamPressure: Optional[ReadingOption]

# AssetReadings type (parametric)
AssetReadings = Dict[str, AssetReadingsByType]

# AssetSensors type
AssetSensors = List[str]
