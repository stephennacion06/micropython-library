"""
battery_monitor.py - Battery Monitoring Library using R1 and R2 for Voltage Divider

Author: Andrew Stephen Nacion
Copyright (c) 2025 Andrew Stephen Nacion

This library measures battery voltage using an ADC and a voltage divider.
Instead of specifying a divider ratio directly, you supply the resistor values:
  - R1: resistor between the battery positive and the ADC input.
  - R2: resistor between the ADC input and ground.

The actual battery voltage is computed as:
  V_bat = V_adc * ((R1 + R2) / R2)

The library also provides an estimate of the battery's state of charge (SOC) 
based on a linear mapping between battery_min_voltage (0% SOC) and battery_max_voltage (100% SOC).

License: MIT License
"""

from machine import ADC
import math

class BatteryMonitor:
    def __init__(self, adc_pin, r1, r2, adc_ref_voltage=3.3,
                 battery_min_voltage=3.0, battery_max_voltage=4.2):
        """
        Initialize the Battery Monitor.

        Args:
            adc_pin (int or machine.ADC): ADC pin number (or ADC object) connected to the voltage divider.
            r1 (float): Resistor value (in ohms) between battery positive and ADC input.
            r2 (float): Resistor value (in ohms) between ADC input and ground.
            adc_ref_voltage (float): ADC reference voltage in volts (default 3.3V).
            battery_min_voltage (float): Voltage corresponding to 0% SOC (default 3.0V).
            battery_max_voltage (float): Voltage corresponding to 100% SOC (default 4.2V).
        """
        if isinstance(adc_pin, int):
            self.adc = ADC(adc_pin)
        else:
            self.adc = adc_pin

        # Compute voltage divider ratio based on resistor values.
        # V_adc = V_bat * (R2/(R1+R2)) so, V_bat = V_adc * ((R1+R2)/R2)
        self.voltage_divider_ratio = (r1 + r2) / r2

        self.adc_ref_voltage = adc_ref_voltage
        self.battery_min_voltage = battery_min_voltage
        self.battery_max_voltage = battery_max_voltage
        self.battery_reading = 0

    def read_adc(self):
        """
        Read the raw ADC value.
        Note: On the Pico, ADC.read_u16() returns a 16-bit value scaled from a 12-bit reading.
        
        Returns:
            int: The ADC reading (0 to 65535).
        """
        return self.adc.read_u16()

    def measure_voltage(self):
        """
        Measure the battery voltage.

        Returns:
            float: The battery voltage in volts.
        """
        # Read ADC value (0-65535)
        adc_val = self.read_adc()
        # Convert ADC reading to voltage at ADC input.
        measured_voltage = (adc_val / 65535) * self.adc_ref_voltage
        # Calculate the actual battery voltage using the computed voltage divider ratio.
        battery_voltage = measured_voltage * self.voltage_divider_ratio
        self.battery_reading = battery_voltage
        return battery_voltage

    def estimate_soc(self):
        """
        Estimate the battery state of charge (SOC) in percent based on a linear mapping.

        Returns:
            float: The estimated SOC percentage (0 to 100%).
        """
        battery_voltage = self.battery_reading
        if battery_voltage <= self.battery_min_voltage:
            return 0.0
        elif battery_voltage >= self.battery_max_voltage:
            return 100.0
        else:
            soc = ((battery_voltage - self.battery_min_voltage) /
                   (self.battery_max_voltage - self.battery_min_voltage)) * 100.0
            return soc
