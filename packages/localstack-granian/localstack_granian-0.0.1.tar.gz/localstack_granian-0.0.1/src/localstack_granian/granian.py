import logging
import signal
import sys
import threading

from rolo.gateway.wsgi import WsgiGateway

from localstack import config
from localstack.runtime.main import print_runtime_information
from localstack.runtime.exceptions import LocalstackExit

LOG = logging.getLogger(__name__)


def run_runtime(runtime):
    try:
        runtime.run()
    except LocalstackExit as e:
        sys.stdout.write(f"Localstack returning with exit code {e.code}. Reason: {e}")
        sys.exit(e.code)
    except Exception as e:
        sys.stdout.write(f"ERROR: the LocalStack runtime exited unexpectedly: {e}\n")
        sys.stdout.flush()
        raise


def create_app():
    from localstack.logging.setup import setup_logging_from_config
    from localstack.runtime import current

    setup_logging_from_config()

    print_runtime_information()

    # signal handler to make sure SIGTERM properly shuts down localstack
    def _terminate_localstack(sig: int, frame):
        sys.stdout.write(f"Localstack runtime received signal {sig}\n")
        sys.stdout.flush()
        runtime.exit(0)

    signal.signal(signal.SIGINT, _terminate_localstack)
    signal.signal(signal.SIGTERM, _terminate_localstack)

    config.GATEWAY_SERVER = "noop"
    runtime = current.initialize_runtime()
    gateway_thread = threading.Thread(target=run_runtime, args=(runtime,))
    gateway_thread.start()

    gateway = runtime.components.gateway
    app = WsgiGateway(gateway)
    return app
