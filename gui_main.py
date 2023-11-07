import sys

from src.bin import Config
from src.gui import start

start(sys.argv, Config.load())
