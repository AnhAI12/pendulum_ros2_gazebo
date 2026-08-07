import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64MultiArray
from sensor_msgs.msg import JointState

class PendulumController(Node):
    def __init__(self):
        super().__init__('pendulum_controller')
        self.publisher_ = self.create_publisher(Float64MultiArray, '/cart_effort_controller/commands', 10)
        self.subscription = self.create_subscription(JointState, '/joint_states', self.joint_state_callback,10)
        self.timer = self.create_timer(1, self.timer_callback)  # Timer to periodically call the callback function
        #variable to store the latest joint state
        self.cart_pos = 0.0
        self.cart_vel = 0.0
        self.pendulum_angle = 0.0
        self.pendulum_vel = 0.0

    def joint_state_callback(self, msg):
        if 'joint_encorder_motor' in msg.name:
            index = msg.name.index('joint_encorder_motor')
            self.cart_pos = msg.position[index]
            self.cart_vel = msg.velocity[index]

        if 'joint_encorder_pendulum' in msg.name:
            index = msg.name.index('joint_encorder_pendulum')
            self.pendulum_angle = msg.position[index]
            self.pendulum_vel = msg.velocity[index]

    def timer_callback(self):
        self.get_logger().info(
            f'cart_pos:{self.cart_pos:.3f}, cart_vel:{self.cart_vel:.3f},'
            f' pendulum_angle:{self.pendulum_angle:.3f}, pendulum_vel:{self.pendulum_vel:.3f}'
        )
        msg = Float64MultiArray()
        msg.data = [1.0]
        self.publisher_.publish(msg)

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
    # rclpy.spin_once(node,  timeout_sec=1)  # Spin once to allow the publisher to initialize
    # node.apply_force(-10.0)  # Apply a force of 10 Newtons
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

