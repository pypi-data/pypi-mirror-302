from TISControlProtocol.Protocols import setup_udp_protocol
from TISControlProtocol.Protocols.udp.ProtocolHandler import (
    TISPacket,
    TISProtocolHandler,
)

from homeassistant.core import HomeAssistant  # type: ignore

# type: ignore
import socket
import logging
from collections import defaultdict
import json
import aiofiles
import asyncio

protocol_handler = TISProtocolHandler()


class TISApi:
    """TIS API class."""

    def __init__(
        self,
        port: int,
        hass: HomeAssistant,
        domain: str,
        devices_dict: dict,
        host: str = "0.0.0.0",
    ):
        """Initialize the API class."""
        self.host = host
        self.port = port
        self.protocol = None
        self.transport = None
        self.hass = hass
        self.config_entries = {}
        self.domain = domain
        self.devices_dict = devices_dict
        self.discovery_packet: TISPacket = protocol_handler.generate_discovery_packet()

    async def connect(self):
        """Connect to the TIS API."""
        self.loop = self.hass.loop
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            self.transport, self.protocol = await setup_udp_protocol(
                self.sock,
                self.loop,
                self.host,
                self.port,
                self.hass,
            )
        except Exception as e:
            logging.error("Error connecting to TIS API %s", e)
            raise ConnectionError

        self.hass.data[self.domain]["discovered_devices"] = []

    async def parse_device_manager_request(self, data: dict) -> None:
        """Parse the device manager request."""
        converted = {
            appliance: {
                "device_id": [int(n) for n in details[0]["device_id"].split(",")],
                "appliance_type": details[0]["appliance_type"]
                .lower()
                .replace(" ", "_"),
                "appliance_class": details[0].get("appliance_class", None),
                "is_protected": bool(int(details[0]["is_protected"])),
                "gateway": details[0]["gateway"],
                "channels": [
                    {
                        "channel_number": int(detail["channel_number"]),
                        "channel_name": detail["channel_name"],
                    }
                    for detail in details
                ],
            }
            for appliance, details in data["appliances"].items()
        }

        grouped = defaultdict(list)
        for appliance, details in converted.items():
            grouped[details["appliance_type"]].append({appliance: details})

        self.config_entries = dict(grouped)
        # add a lock module config entry
        self.config_entries["lock_module"] = {
            "password": data["configs"]["lock_module_password"]
        }
        # return response
        return self.config_entries
        # await self.update_entities()

    # async def get_entities(self, platform: str = None) -> list:
    #     """Get the stored entities."""
    #     try:
    #         with open("appliance_data.json", "r") as f:
    #             data = json.load(f)
    #             await self.parse_device_manager_request(data)
    #     except FileNotFoundError:
    #         with open("appliance_data.json", "w") as f:
    #             pass
    #     await self.parse_device_manager_request(data)
    #     entities = self.config_entries.get(platform, [])
    #     return entities

    async def save_devices(self, devices):
        # Dump to local file
        async with aiofiles.open("devices_data.json", "w") as f:
            await f.write(json.dumps({"devices": devices}, indent=4))

    async def load_devices(self) -> list[dict]:
        # Load from local file
        async with aiofiles.open("devices_data.json", "r") as f:
            devices = json.loads(await f.read())
        return devices

    async def scan_devices(self, prodcast_attempts=10):
        """Scan for devices."""
        # clear the previous discovered devices
        self.hass.data[self.domain]["discovered_devices"] = []
        # send dicover packet
        for _ in range(prodcast_attempts):
            await self.protocol.sender.broadcast_packet(self.discovery_packet)
            await asyncio.sleep(1)
        # fetch the devices
        devices = [
            {
                "device_id": device["device_id"],
                "device_type_code": device["device_type"],
                "device_type_name": self.devices_dict.get(
                    tuple(device["device_type"]), tuple(device["device_type"])
                ),
                "gateway": device["source_ip"],
            }
            for device in self.hass.data[self.domain]["discovered_devices"]
        ]
        # dump to local file
        await self.save_devices(devices)

    async def get_entities(self):
        # load devices
        devices = await self.load_devices()
        logging.error("discovered devices : %s ", devices)
        logging.error(
            " devices id type: %s ",
            type(devices[0]["device_id"]) if devices else "No devices found",
        )
