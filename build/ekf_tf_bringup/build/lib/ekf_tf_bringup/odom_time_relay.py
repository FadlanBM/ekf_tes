import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry

class OdomTimeRelay(Node):
    def __init__(self):
        super().__init__('odom_time_relay')
        # Subscribe to the original raw odometry
        self.subscription = self.create_subscription(
            Odometry,
            '/teensy_odom_raw',
            self.odom_callback,
            10)
        
        # Publish to a new synchronized topic
        self.publisher = self.create_publisher(
            Odometry, 
            '/odom_sync', 
            10)
            
        self.get_logger().info("Odom Time Relay started. Relaying /teensy_odom_raw to /odom_sync with PC timestamp.")

    def odom_callback(self, msg):
        # Overwrite the timestamp with the PC's current ROS time
        msg.header.stamp = self.get_clock().now().to_msg()
        # Publish the updated message
        self.publisher.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = OdomTimeRelay()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
