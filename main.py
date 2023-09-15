from src.bin import CliBin, Config
from src.cli import MainCli

config = Config.load()
bin = CliBin(config)


MainCli.run(bin)
