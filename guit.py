from src.config import Config
from src.mod_tool import ModTool
from src.gui.main import start_gui
from src.service import ModService
import sys

config = Config.load()
tool = ModTool(config)
service = ModService(tool)
argv: list[str] = sys.argv
start_gui(argv, service)
