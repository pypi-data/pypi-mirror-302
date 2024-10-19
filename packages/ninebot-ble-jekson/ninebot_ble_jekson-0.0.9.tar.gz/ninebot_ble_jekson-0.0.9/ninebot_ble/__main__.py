"""Command-line client for reading Ninebot scooter registers

Running with no arguments will start the ninebot sensor and dump all data.

It is also possible to only read specific registers using flags, see --help.
"""

import argparse
import asyncio
import logging
import time
import os
from typing import Any

from home_assistant_bluetooth import BluetoothServiceInfo

from ninebot_ble import (
    BmsIdx,
    CtrlIdx,
    NinebotClient,
    async_scooter_scan,
    get_register_desc,
    iter_register,
)

logger = logging.getLogger(__name__)


def clear():
    os.system('cls')


def dump_reg(name: str, val: Any, unit: str) -> None:
    print("\033[1A", end="")
    print("\033[1A", end="")
    print(f"{name:<10}: {val:.0f} {unit}")
    print('|' * abs(int(val/10)))



async def main() -> None:
    logging.basicConfig(format="%(asctime)s %(levelname)s %(message)s", level=logging.INFO)
    logging.getLogger("bleak.backends.bluezdbus.manager").level = logging.WARNING
    logging.getLogger("bleak.backends.bluezdbus.client").level = logging.WARNING

    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter, description=__doc__)

    arg_mapping: dict[str, BmsIdx | CtrlIdx] = {}
    for idx in iter_register(CtrlIdx, BmsIdx):
        arg = "_".join(str(idx).lower().split())
        arg_mapping[arg] = idx
        parser.add_argument("--" + arg, action="store_true", help=f"read {str(idx).lower()}")

    args = parser.parse_args()

    device, advertisement = await async_scooter_scan()

    indices: list[BmsIdx | CtrlIdx] = []
    for idx_arg, idx in arg_mapping.items():
        if args.__dict__.get(idx_arg):
            indices.append(idx)

    client = NinebotClient()
    try:
        await client.connect(device)
        print("asd")
        for i in range(100):
            current = await client.read_reg('Battery current')
            voltage = await client.read_reg('Battery voltage')
            dump_reg("Power", current*voltage, "W")
            time.sleep(0.1)
    finally:
        await client.disconnect()


def entrypoint() -> None:
    asyncio.run(main())


if __name__ == "__main__":
    entrypoint()
