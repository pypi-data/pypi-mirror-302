from typing import Any

class Commands:
  def __init__(self, sdk):
    self.sdk = sdk

  def availableCommands(self) -> list[Any]:
    """
    Returns the available commands to call. You can use this method to connect your plugin with other plugins, or with other Qatium components
    """
    return self.sdk.commands.availableCommands()
