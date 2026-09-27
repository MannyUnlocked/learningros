import rclpy
from rclpy.node import Node
from std_msgs.msg import Bool, Int32

class MotorTempNode(Node):
    def __init__(self):
        super().__init__('motor_temp')
        self.motor_state= Bool()
        self.pub_= self.create_publisher(Bool,"motor_state",10)
        self.create_subscription(Int32, "temp_reading", self.temp_callback, 10)
        self.get_logger().info('Node Initialised')

    def temp_callback(self, msg):
        '''this is how you callback all the temp readings when they drop'''
        temp=msg.data
        if temp<=60:
            self.get_logger().info(f'Motor Temperature is {temp}')
            self.motor_state.data= True
            self.pub_.publish(self.motor_state)

def main(args=None):
    rclpy.init(args=args)
    node = MotorTempNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()


