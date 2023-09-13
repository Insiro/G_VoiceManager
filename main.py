from src.config import Config
from src.mod_tool import ModTool
from src.cli import MainCli
from src.service import ModService

config = Config.load()
tool = ModTool(config)
service = ModService(tool)
MainCli.run(service)
