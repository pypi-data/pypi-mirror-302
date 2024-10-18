import threading

from localstack import config
from rolo.gateway.gateway import Gateway
from localstack.runtime.server import RuntimeServer
from localstack.runtime.server.core import RuntimeServerPlugin


class NoopRuntimeServerPlugin(RuntimeServerPlugin):
    name = "noop"

    def load(self, *args, **kwargs) -> RuntimeServer:
        return NoopRuntimeServer()


class NoopRuntimeServer(RuntimeServer):
    shutdown_event: threading.Event

    def __init__(self):
        self.shutdown_event = threading.Event()

    def register(
        self,
        gateway: Gateway,
        listen: list[config.HostAndPort],
        ssl_creds: tuple[str, str] | None = None,
    ):
        pass

    def run(self):
        self.shutdown_event.wait()

    def shutdown(self):
        self.shutdown_event.set()
