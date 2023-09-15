from src.config import Config
from src.cli import MainCli

from src.bin import CliBin

config = Config.load()
bin = CliBin(config)


MainCli.run(bin)
