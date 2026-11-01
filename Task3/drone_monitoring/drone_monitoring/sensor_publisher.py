"""Sensor publisher node: simulates altitude, battery and temperature.

Node name : drone_sensor_publisher
Topics    : /drone/altitude, /drone/battery, /drone/temperature (Float32, 1 Hz)

Initial conditions are ROS parameters, so each test case can be triggered
from the command line without editing code, e.g.:
    ros2 run drone_monitoring sensor_publisher --ros-args -p battery_start:=15.0
"""
import math
import random

import rclpy
from rclpy.node import Node
from rcl_interfaces.msg import ParameterDescriptor
from std_msgs.msg import Float32

PUBLISH_PERIOD_S = 1.0  # 1 Hz


class DroneSensorPublisher(Node):
    def __init__(self):
        super().__init__('drone_sensor_publisher')

        # dynamic_typing lets "-p battery_start:=15" (int) work as well as 15.0
        d = ParameterDescriptor(dynamic_typing=True)
        self.declare_parameter('altitude_base', 15.0, d)         # m, centre of oscillation
        self.declare_parameter('altitude_amplitude', 10.0, d)    # m (default peak = 25 m)
        self.declare_parameter('altitude_period', 60.0, d)       # s per full climb/descent
        self.declare_parameter('battery_start', 100.0, d)        # %
        self.declare_parameter('battery_drain', 0.5, d)          # % per second
        self.declare_parameter('temperature_base', 40.0, d)      # deg C
        self.declare_parameter('temperature_amplitude', 3.0, d)  # deg C
        self.declare_parameter('temperature_noise', 0.3, d)      # deg C

        def p(name):
            return float(self.get_parameter(name).value)

        self.alt_base = p('altitude_base')
        self.alt_amp = p('altitude_amplitude')
        self.alt_period = p('altitude_period')
        self.battery = min(100.0, max(0.0, p('battery_start')))
        self.drain = p('battery_drain')
        self.temp_base = p('temperature_base')
        self.temp_amp = p('temperature_amplitude')
        self.temp_noise = p('temperature_noise')

        self.alt_pub = self.create_publisher(Float32, '/drone/altitude', 10)
        self.bat_pub = self.create_publisher(Float32, '/drone/battery', 10)
        self.temp_pub = self.create_publisher(Float32, '/drone/temperature', 10)

        self.t = 0.0
        self.timer = self.create_timer(PUBLISH_PERIOD_S, self.publish_sensors)
        self.get_logger().info(
            f'Sensor publisher started (battery={self.battery:.1f}%, '
            f'altitude_base={self.alt_base:.1f} m, temperature_base={self.temp_base:.1f} C)')

    def publish_sensors(self):
        # Altitude: smooth sinusoidal climb and descent, never below ground.
        altitude = self.alt_base + self.alt_amp * math.sin(
            2.0 * math.pi * self.t / self.alt_period)
        altitude = max(0.0, altitude)

        # Battery: steady drain, clamped to 0-100.
        self.battery = min(100.0, max(0.0, self.battery - self.drain))

        # Temperature: slow oscillation plus a little random noise.
        temperature = (self.temp_base
                       + self.temp_amp * math.sin(2.0 * math.pi * self.t / 45.0)
                       + random.uniform(-self.temp_noise, self.temp_noise))

        self.alt_pub.publish(Float32(data=float(altitude)))
        self.bat_pub.publish(Float32(data=float(self.battery)))
        self.temp_pub.publish(Float32(data=float(temperature)))

        self.get_logger().info(
            f'alt={altitude:.1f} m  bat={self.battery:.1f} %  temp={temperature:.1f} C')
        self.t += PUBLISH_PERIOD_S


def main(args=None):
    rclpy.init(args=args)
    node = DroneSensorPublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
