from typing import Any, Callable

class AssetStatus:
  OPEN = 'open'
  CLOSED = 'closed'
  ACTIVE = 'active'

class Network:
  def __init__(self, sdk):
    self.sdk = sdk

  def getValves(self, predicate: Callable) -> list[Any]:
    """
    Retrieve all valves that match a predicate.

    Args:
        predicate (function): A function that takes an asset and returns a boolean value.

    Returns:
        list[Asset]: A list of assets that match the predicate.
    """
    return self.sdk.network.getValves(predicate)

  def setStatus(self, assetId: str, status: str):
    """
    Set the status of an asset.

    Args:
        assetId (str): The unique identifier of the asset to set the status for.
        status (OPEN | CLOSED): The new status of the asset.
    """
    return self.sdk.network.setStatus(assetId, status)
