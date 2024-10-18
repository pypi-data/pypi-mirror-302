from typing import Any
from pyodide import ffi

class UI:
  def __init__(self, sdk):
    self.sdk = sdk

  def sendMessage(self, message: Any):
    """
    Send a message to the user interface.

    Args:
        message (str): The message to send to the user interface.
    """
    self.sdk.ui.sendMessage(ffi.to_js(message))
