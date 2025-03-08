"""
lidar_lib.py - LiDAR Sensor Library for UART Communication and LED Feedback

Author: Andrew Stephen Nacion
Copyright (c) 2025 Andrew Stephen Nacion
Licensed under the MIT License. See LICENSE file in the project root for full license information.

This library provides a LidarSensor class to handle LiDAR data acquisition via UART,
with support for asynchronous tasks and LED feedback.

Features:
    - Reading LiDAR data packets with checksum validation.
    - Asynchronous polling of LiDAR data.
    - LED blink feedback.
    - Configurable callback for handling LiDAR data.

License: MIT License
"""

import machine
import uasyncio as asyncio

class LidarSensor:
    """
    LidarSensor class for reading LiDAR data via UART and providing LED feedback.

    Configuration parameters:
      uart_id (int): The UART port to use (default: 1).
      baud_rate (int): Baud rate for UART communication (default: 115200).
      uart_tx_pin (int): The TX pin number (default: 4).
      uart_rx_pin (int): The RX pin number (default: 5).
      led_pin (int): The on-board LED pin (default: 25).
    """
    
    def __init__(self, uart_id=1, baud_rate=115200, uart_tx_pin=4, uart_rx_pin=5, led_pin=25):
        # Initialize UART for LiDAR data and configure the LED pin.
        self.uart = machine.UART(uart_id, baudrate=baud_rate,
                                 tx=machine.Pin(uart_tx_pin),
                                 rx=machine.Pin(uart_rx_pin))
        self.led = machine.Pin(led_pin, machine.Pin.OUT)
    
    def read_lidar(self):
        """
        Reads a 9-byte packet from the LiDAR sensor via UART.
        
        Packet format:
          Byte 0: 0x59 (header)
          Byte 1: 0x59 (header)
          Byte 2: Distance low byte
          Byte 3: Distance high byte
          Byte 4: Strength low byte
          Byte 5: Strength high byte
          Byte 6-7: Temperature bytes (ignored)
          Byte 8: Checksum (sum of bytes 0-7) & 0xFF

        Returns:
          tuple: (distance, strength) if a valid packet is received,
                 or None if the packet is incomplete or invalid.
        """
        if self.uart.any() < 9:
            return None
        data = self.uart.read(9)
        if data is None or len(data) < 9:
            return None
        if data[0] != 0x59 or data[1] != 0x59:
            return None
        if (sum(data[0:8]) & 0xFF) != data[8]:
            return None
        # Parse distance and strength (little-endian format)
        distance = data[2] | (data[3] << 8)
        strength = data[4] | (data[5] << 8)
        return distance, strength

    async def update(self, callback=None, poll_interval_ms=10):
        """
        Continuously polls the UART for new LiDAR data.
        
        Args:
          callback (function): Optional callback that accepts (distance, strength).
                               If not provided, the values are printed.
          poll_interval_ms (int): Polling interval in milliseconds (default: 10ms).
        """
        while True:
            result = self.read_lidar()
            if result is not None:
                distance, strength = result
                if callback:
                    callback(distance, strength)
                else:
                    print("Dist: {} Strength: {}".format(distance, strength))
            await asyncio.sleep_ms(poll_interval_ms)

    async def blink_led(self, blink_interval_ms=100):
        """
        Blinks the on-board LED to provide visual feedback.
        
        Args:
          blink_interval_ms (int): Interval in milliseconds for the LED blink (default: 100ms).
        """
        while True:
            self.led.value(0)
            await asyncio.sleep_ms(blink_interval_ms)
            self.led.value(1)
            await asyncio.sleep_ms(blink_interval_ms)

async def run_lidar_tasks(lidar_sensor, callback=None):
    """
    Runs the LiDAR update and LED blink tasks concurrently.
    
    Args:
      lidar_sensor (LidarSensor): An instance of LidarSensor.
      callback (function): Optional callback for handling LiDAR data updates.
    """
    await asyncio.gather(
        lidar_sensor.update(callback=callback),
        lidar_sensor.blink_led()
    )

def main():
    """
    Main function that creates a LidarSensor instance and runs the asynchronous tasks.
    """
    sensor = LidarSensor()
    asyncio.run(run_lidar_tasks(sensor))

# If run directly, execute the main function.
if __name__ == '__main__':
    main()
