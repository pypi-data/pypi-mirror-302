import ipih

from pih.consts.hosts import Hosts
from pih.collections.service import ServiceDescription

NAME: str = "IOTDevices"

HOST = Hosts.WS255

MODULES: tuple[str, ...] = ("tinytuya",)

VERSION: str = "0.141"

API_REGION: str = "eu"
API_KEY: str = "guj4wmavqukcytha3crr"
API_SECRET: str = "339ad2c6379e4fb988d0c2cc97882ffa"

SD: ServiceDescription = ServiceDescription(
    name=NAME,
    description="IOT Devices service",
    host=HOST.NAME,
    use_standalone=True,
    host_changeable=True,
    standalone_name="iot",
    version=VERSION,
    packages=MODULES,
)
