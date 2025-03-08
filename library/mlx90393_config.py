"""
mlx90393_config.py - Configuration Library for MLX90393 Magnetometer Sensor

Author: Andrew Stephen Nacion
Copyright (c) 2025 Andrew Stephen Nacion
Licensed under the MIT License. See LICENSE file in the project root for full license information.

This library provides helper functions for configuring the MLX90393 magnetometer sensor,
including:
    - configure_sensor(sensor, ...): Configures the sensor with the provided settings.
    - get_possible_configurations(): Returns a dictionary of configuration parameters 
      and their possible numeric values.
    - get_default_calibration(): Returns the sensor's default calibration values.
    - get_current_calibration(): Returns the current calibration settings saved in RAM.
    - save_default_calibration(calibration, filename="calibration.json"): Saves the calibration
      settings to a file.
    - load_default_calibration(filename="calibration.json"): Loads the calibration settings from a file.

License: MIT License
"""

import ujson  # Use MicroPython's ujson for JSON handling
from micropython_mlx90393 import GAIN_1X, RESOLUTION_3, FILTER_7, OSR_3

# Global variable to store the current calibration in RAM.
CURRENT_CALIBRATION = None

def configure_sensor(sensor, gain, resolution_x, resolution_y, resolution_z, digital_filter, oversampling):
    """
    Configure the MLX90393 sensor with the given settings.
    """
    sensor.gain = gain
    sensor.resolution_x = resolution_x
    sensor.resolution_y = resolution_y
    sensor.resolution_z = resolution_z
    sensor.digital_filter = digital_filter
    sensor.oversampling = oversampling

    global CURRENT_CALIBRATION
    CURRENT_CALIBRATION = {
        "gain": gain,
        "resolution_x": resolution_x,
        "resolution_y": resolution_y,
        "resolution_z": resolution_z,
        "digital_filter": digital_filter,
        "oversampling": oversampling,
    }

def get_possible_configurations():
    """
    Returns a dictionary containing the possible numeric configuration options
    for the MLX90393 sensor.
    """
    config_options = {
        "gain": [0, 1, 2, 3, 4, 5, 6, 7],
        "resolution_x": [0, 1, 2, 3],
        "resolution_y": [0, 1, 2, 3],
        "resolution_z": [0, 1, 2, 3],
        "digital_filter": [0, 1, 2, 3, 4, 5, 6, 7],
        "oversampling": [0, 1, 2, 3]
    }
    return config_options

def get_default_calibration():
    """
    Returns the default calibration values using the sensor's built-in defaults.
    """
    return {
        "gain": GAIN_1X,
        "resolution_x": RESOLUTION_3,
        "resolution_y": RESOLUTION_3,
        "resolution_z": RESOLUTION_3,
        "digital_filter": FILTER_7,
        "oversampling": OSR_3,
    }

def get_current_calibration():
    """
    Returns the current calibration settings stored in RAM.
    If no calibration has been set, it returns the default calibration.
    """
    global CURRENT_CALIBRATION
    if CURRENT_CALIBRATION is None:
        CURRENT_CALIBRATION = get_default_calibration()
    return CURRENT_CALIBRATION

def save_default_calibration(calibration, filename="calibration.json"):
    """
    Save the current calibration to a file.
    """
    try:
        with open(filename, "w") as f:
            f.write(ujson.dumps(calibration))
        print("Default calibration saved to", filename)
    except Exception as e:
        print("Error saving calibration:", e)

def load_default_calibration(filename="calibration.json"):
    """
    Load the calibration from a file.
    """
    try:
        with open(filename, "r") as f:
            calibration = ujson.loads(f.read())
        print("Default calibration loaded from", filename)
        return calibration
    except Exception as e:
        print("Error loading calibration:", e)
        print("Using built-in default calibration values.")
        return get_default_calibration()

if __name__ == "__main__":
    # For testing: print all configuration options.
    options = get_possible_configurations()
    for key, values in options.items():
        print(f"{key}: {values}")

    # Test saving the default calibration.
    default_cal = get_default_calibration()
    save_default_calibration(default_cal)

    # Test loading the default calibration.
    loaded_cal = load_default_calibration()
    print("Loaded calibration:", loaded_cal)

    # Test getting the current calibration.
    current_cal = get_current_calibration()
    print("Current calibration:", current_cal)
