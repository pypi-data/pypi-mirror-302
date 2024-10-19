import enum
import logging

from bleak.backends.device import BLEDevice
from bluetooth_sensor_state_data import BluetoothData
from home_assistant_bluetooth import BluetoothServiceInfo
from sensor_state_data import SensorUpdate

from .register import BmsIdx, CtrlIdx, get_register_desc, iter_register
from .serial_parser import SerialParser
from .transport import NinebotClient

_LOGGER = logging.getLogger(__name__)


class NinebotBleSensor(BluetoothData):
    """Ninebot scooter sensor.

    Primary for Home Assistant integration.
    """

    def __init__(self) -> None:
        super().__init__()

        self.client = NinebotClient()
        self.device: BLEDevice | None = None

    async def disconnect(self) -> None:
        """Disconnect scooter."""
        if self.client is not None:
            await self.client.disconnect()

    async def async_poll(self, device: BLEDevice) -> SensorUpdate:
        """Poll all data from Scooter."""
        print("Connected:", self.client.is_connected)
        if not self.client.is_connected or self.device is None or self.device != device:
            await self.client.disconnect()
            self.client = NinebotClient()
            await self.client.connect(device)
            self.device = device

        serial = await self.client.read_reg(CtrlIdx.NB_INF_SN)
        try:
            parsed_sn = SerialParser(serial)
            self.set_title(str(parsed_sn))
            self.set_device_type(str(parsed_sn))
            self.set_device_hw_version(
                f"Rev {parsed_sn.product_revision}, {parsed_sn.production_date.year}/{parsed_sn.production_date.month}"
            )
        except ValueError as e:
            _LOGGER.warn("Failed to parse scooter serial number: %s", e)
            self.set_title(device.name or device.address)
            self.set_device_type("Ninebot scooter")

        sw_version = await self.client.read_reg(CtrlIdx.NB_FW_VER)
        self.set_device_sw_version(sw_version)

        for idx in iter_register(CtrlIdx, BmsIdx):
            entry = get_register_desc(idx)
            val = await self.client.read_reg(idx)
            if isinstance(val, enum.Enum):
                val = val.name
            self.update_sensor(str(idx), entry.unit, val, entry.device_class, str(idx))

        return self._finish_update()

    def supported(self, data: BluetoothServiceInfo) -> bool:
        """Return True if the device is supported.

        Override.
        """
        self._start_update(data)
        return data.manufacturer_id == 16974

    def _start_update(self, service_info: BluetoothServiceInfo) -> None:
        """Update from BLE advertisement data.

        Override.
        """
        self.set_device_manufacturer("Segway")
        self.set_device_name(service_info.name)
