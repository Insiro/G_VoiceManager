import sys
from argparse import ArgumentParser

from src.bin import Config

parser = ArgumentParser()
parser.add_argument("--cli", action="store_true", default=False)
parser.add_argument("-c", "--config", default=None)

args = parser.parse_args()


if args.cli:
    from src.cli import start


else:
    from src.gui import start

start(sys.argv, Config.load(args.config))
