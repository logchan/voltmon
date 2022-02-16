import logging
import time
from argparse import ArgumentParser
from typing import Callable, List, Optional

import psutil
import serial
import serial.tools.list_ports

class VoltmonServer:
    def __init__(self,
        port: Optional[str],
        baudrate: int,
        pins: List[int],
        getters: List[Callable[[], float]],
        reconn_wait: float = 2,
        update_wait: float = 0.5,
        ) -> None:

        self.port = port
        self.baudrate = baudrate
        self.pins = pins
        self.getters = getters
        self.reconn_wait = reconn_wait
        self.update_wait = update_wait

        self.conn = None

    def loop(self):
        while True:
            if self.conn is None:
                wait = self.connect()
            else:
                wait = self.update()
            time.sleep(wait)

    def connect(self) -> float:
        port = self.port
        if port is None:
            ports = serial.tools.list_ports.comports()
            if len(ports) > 0:
                port = ports[0].name
            else:
                return self.reconn_wait

        try:
            logging.info(f"Connecting to: {port}")
            self.conn = serial.Serial(port, self.baudrate, timeout=1)
            if not self.conn.is_open:
                raise ValueError(f"Connection is not open after creation")
            return self.update_wait
        except Exception as ex:
            logging.error(f"Faild connecting to {port}: {repr(ex)}")
            self.conn = None

            return self.reconn_wait

    def update(self) -> float:
        try:
            pins = self.pins
            values = [func() for func in self.getters]
            updates = list(zip(pins, values))
            
            logging.debug(f"Update: {updates}")
            
            for pin, value in updates:
                self.write_update(pin, self.convert_percentage(value))
            
            return 0.5
        except Exception as ex:
            logging.error(f"Failed sending data: {repr(ex)}")
            self.conn = None
            return 2

    def write_update(self, pin, value):
        if not self.conn.is_open:
            raise ValueError("Connection is closed")

        cmd = bytearray([0x22, 0x33, 0x01, pin, value, 0x00, 0x00, 0x00])
        if self.conn.write(cmd) != 8:
            raise ValueError("Number of sent bytes not equals to 8")

    @staticmethod
    def convert_percentage(v):
        return max(0, min(255, round(255 * v / 100)))


def main():
    parser = ArgumentParser()
    parser.add_argument("-p", "--port", help="Manually specify a serial port", default=None)
    parser.add_argument("-b", "--baudrate", help="Baudrate, must match client", default=9600)
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose logging")
    parser.add_argument("--cpu_pin", type=int, default=0, help="The index of the pin (NOT its number) in your pin_ids array to use for CPU")
    parser.add_argument("--ram_pin", type=int, default=3, help="The index of the pin (NOT its number) in your pin_ids array to use for RAM")

    args = parser.parse_args()

    logging.basicConfig(
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[logging.StreamHandler()],
        level=logging.DEBUG if args.verbose else logging.INFO)

    server = VoltmonServer(args.port, args.baudrate,
        [
            args.cpu_pin,
            args.ram_pin
        ],
        [
            lambda: psutil.cpu_percent(1),
            lambda: psutil.virtual_memory().percent
        ])
    try:
        server.loop()
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()
