"""Warning publisher node: turns /drone/status into human-readable warnings.

Node name : drone_warning_publisher
Subscribes: /drone/status (String)
Publishes : /drone/warnings (String)
"""
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

WARNING_TEXT = {
    'LOW BATTERY': '[WARNING] Battery level is critically low!',
    'OVERHEATING': '[WARNING] Drone temperature exceeds safe limit!',
    'ALTITUDE LIMIT EXCEEDED': '[WARNING] Drone altitude exceeded the configured limit!',
}


def build_warnings(status):
    """Map a status string to a list of warning/info messages."""
    status = status.strip()
    if status == 'NORMAL':
        return ['No active warnings']
    if status == 'WAITING FOR SENSOR DATA':
        return ['Waiting for telemetry']
    warnings = []
    for condition in (c.strip() for c in status.split(',')):
        warnings.append(WARNING_TEXT.get(condition, f'[WARNING] Unknown condition: {condition}'))
    return warnings


class DroneWarningPublisher(Node):
    def __init__(self):
        super().__init__('drone_warning_publisher')
        self.create_subscription(String, '/drone/status', self.on_status, 10)
        self.warning_pub = self.create_publisher(String, '/drone/warnings', 10)
        self.get_logger().info('Warning publisher started')

    def on_status(self, msg):
        warnings = build_warnings(msg.data)
        for w in warnings:
            self.get_logger().info(w)
        self.warning_pub.publish(String(data=' | '.join(warnings)))


def main(args=None):
    rclpy.init(args=args)
    node = DroneWarningPublisher()
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
