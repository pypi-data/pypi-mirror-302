from .window_tools import WindowTools
from .err_messages import ErrMessages
from .action_assets import ActionAssets
from .calculate_window_position import CalculateWindowPosition

class WindowAsset:
    """ A group of classes meant to ease window management """

    def __init__(self) -> None:
        super(WindowAsset, self).__init__()
        self.__version__ = "1.0.0"
        self.window_tools = WindowTools
        self.err_messages = ErrMessages
        self.action_assets = ActionAssets
        self.calculate_window_position = CalculateWindowPosition


if __name__ == "__main__":
    print(f"WindowAsset = {dir(WindowAsset())}")
