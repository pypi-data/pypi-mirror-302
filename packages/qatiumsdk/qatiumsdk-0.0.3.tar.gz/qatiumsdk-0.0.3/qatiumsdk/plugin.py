from typing import Protocol

class Plugin(Protocol):
  def run(self) -> None:
    pass

  def onMessage(self, message) -> None:
    pass
