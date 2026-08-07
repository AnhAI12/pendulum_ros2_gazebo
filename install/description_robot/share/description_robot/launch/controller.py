import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64MultiArray

class PendulumController(Node):
    def __init__(self):
        super().__init__('pendulum_controller')
        self.publisher_ = self.create_publisher(Float64MultiArray, '/cart_effort_controller/commands', 10)

    def apply_force(self,force_newtons: float):
        # Create a Float64MultiArray message
        msg = Float64MultiArray()
        msg.data = [force_newtons]  # Assuming the controller expects a single force value
        # Publish the message
        self.publisher_.publish(msg)
        self.get_logger().info(f'Applied force: {force_newtons} N')

def main(args=None):
    rclpy.init(args=args)
    node = PendulumController()
    # Example usage: apply a force of 10 Newtons
    rclpy.spin_once(node,  timeout_sec=1)  # Spin once to allow the publisher to initialize
    node.apply_force(10.0)  # Apply a force of 10 Newtons
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

