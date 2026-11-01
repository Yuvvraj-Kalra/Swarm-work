"""Telemetry monitor node: stores latest sensor values and publishes status.

Node name : drone_telemetry_monitor
Subscribes: /drone/altitude, /drone/battery, /drone/temperature (Float32)
Publishes : /drone/status (String, 1 Hz)
"""
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32, String

BATTERY_MIN = 20.0       # % - below this is LOW BATTERY
TEMPERATURE_MAX = 60.0   # deg C - above this is OVERHEATING
ALTITUDE_MAX = 30.0      # m - above this is ALTITUDE LIMIT EXCEEDED
WAITING = 'WAITING FOR SENSOR DATA'


def evaluate_status(altitude, battery, temperature):
    """Return the status string for the given readings (None = not received)."""
    if altitude is None or battery is None or temperature is None:
        return WAITING
    conditions = []
    if battery < BATTERY_MIN:
        conditions.append('LOW BATTERY')
    if temperature > TEMPERATURE_MAX:
        conditions.append('OVERHEATING')
    if altitude > ALTITUDE_MAX:
        conditions.append('ALTITUDE LIMIT EXCEEDED')
    return ', '.join(conditions) if conditions else 'NORMAL'


class DroneTelemetryMonitor(Node):
    def __init__(self):
        super().__init__('drone_telemetry_monitor')
        self.altitude = None
        self.battery = None
        self.temperature = None

        self.create_subscription(Float32, '/drone/altitude', self.on_altitude, 10)
        self.create_subscription(Float32, '/drone/battery', self.on_battery, 10)
        self.create_subscription(Float32, '/drone/temperature', self.on_temperature, 10)
        self.status_pub = self.create_publisher(String, '/drone/status', 10)

        self.timer = self.create_timer(1.0, self.report)
        self.get_logger().info('Telemetry monitor started')

    def on_altitude(self, msg):
        self.altitude = msg.data

    def on_battery(self, msg):
        self.battery = msg.data

    def on_temperature(self, msg):
        self.temperature = msg.data

    def report(self):
        status = evaluate_status(self.altitude, self.battery, self.temperature)

        def fmt(v, unit):
            return 'N/A' if v is None else f'{v:.1f} {unit}'

        self.get_logger().info(
            '\nDrone Telemetry\n\n'
            f'Altitude       : {fmt(self.altitude, "m")}\n'
            f'Battery        : {fmt(self.battery, "%")}\n'
            f'Temperature    : {fmt(self.temperature, "°C")}\n'
            f'Status         : {status}')

        self.status_pub.publish(String(data=status))


def main(args=None):
    rclpy.init(args=args)
    node = DroneTelemetryMonitor()
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
