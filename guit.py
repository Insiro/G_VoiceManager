import sys

from src.config import Config
from src.gui.main import start_gui

argv: list[str] = sys.argv
config = Config.load()
start_gui(argv, config)
