from src.config import Config
from src.mod_tool import ModTool
from src.cli import MainCli
from src.service import DirService

config = Config.load()
tool = ModTool(config)
service = DirService(tool)
MainCli.run(service)
