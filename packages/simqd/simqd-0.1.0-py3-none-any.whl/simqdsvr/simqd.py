import os
import logging
import signal

import sigterm
import click
from zenutils import importutils

__all__ = [
    "main",
]
_logger = logging.getLogger(__name__)

config = {
    "service-providers": [],
    "base-url": None,
    "api-key": None,
    "workers": None,
}


def update_config(service_providers, base_url, api_key, workers):
    if service_providers:
        config["service-providers"] = service_providers
    if base_url:
        config["base-url"] = base_url
    if api_key:
        config["api-key"] = api_key
    if workers:
        config["workers"] = workers


def load_config():
    if not config["service-providers"]:
        config["service-providers"] = os.environ.get("SIMQD_SERVICE_PROVIDERS")
    if not config["base-url"]:
        config["base-url"] = os.environ.get("SIMQ_BASE_URL")
    if not config["api-key"]:
        config["api-key"] = os.environ.get("SIMQ_API_KEY")
    if not config["workers"]:
        config["workers"] = os.environ.get("SIMQ_WORKERS", 5)


def worker():
    _logger.warning("Press Ctrl+C to stop...")
    service_providers = config["service-providers"]
    base_url = config["base-url"]
    api_key = config["api-key"]
    workers = config["workers"]
    # 检查必需参数
    if not service_providers:
        _logger.error(
            "You must provide service provider class names via --service-provider parameter or SIMQD_SERVICE_PROVIDERS environment..."
        )
    if not base_url:
        _logger.error(
            "You must provide simq base_url via --base-url parameter or SIMQ_BASE_URL environment..."
        )
    if (not service_providers) or (not base_url):
        return
    # 启动服务实例
    service_provider_instances = []
    for service_provider in service_providers:
        service_provider_class = importutils.import_from_string(service_provider)
        if not service_provider_class:
            _logger.warning(f"Service {service_provider} can not load...")
            continue
        service_provider_instance = service_provider_class(
            workers=workers,
            base_url=base_url,
            api_key=api_key,
        )
        service_provider_instance.start()
        service_provider_instances.append(service_provider_instance)
        _logger.warning(f"Service {service_provider} started with workers={workers}...")
    # 等待
    for service_provider_instance in service_provider_instances:
        service_provider_instance.wait_forever()


@click.command()
@click.option("-p", "--service-provider", multiple=True)
@click.option("-s", "--base-url")
@click.option("-a", "--api-key")
@click.option("-w", "--workers", type=int)
def main(service_provider, base_url, api_key, workers):
    update_config(
        service_providers=service_provider,
        base_url=base_url,
        api_key=api_key,
        workers=workers,
    )
    load_config()
    sigterm.setup()
    sigterm.setup(signal.SIGINT)
    sigterm.register_worker(worker)
    sigterm.execute()


if __name__ == "__main__":
    main()
