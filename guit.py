import sys

from src.bin import Config
from src.gui.main import start_gui

argv: list[str] = sys.argv
config = Config.load()
start_gui(argv, config)
