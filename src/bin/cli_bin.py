from src.bin.bin import Bin
from src.config import Config
from src.service import ConfigService


class CliBin(Bin):
    @property
    def conf_service(self):
        return self._conf_service

    def __init__(self, config: Config) -> None:
        self._conf_service = ConfigService(config)
        super().__init__(config)
