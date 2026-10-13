import rclpy
from rclpy.node import Node
from std_msgs.msg import Bool
from std_srvs.srv import SetBool

class RobotSafetyCtrl(Node):
    '''A demo node for a robot safety system checker'''

    def __init__(self):
        super().__init__('robot_safety_control')

        self.loc_flag = False
        self.robot_flag = False

        self.loc_init_sub_ = self.create_subscription(Bool, 'loc_ready', self.loc_cb, 10)
        self.robot_init_sub_ = self.create_subscription(Bool, 'robot_ready', self.robot_cb, 10)
        self.cli_ = self.create_client(SetBool, 'motor_sft_ctrl')

        while not self.cli_.wait_for_service(1.0):
            self.get_logger().warning('Motor Control Server NOT available')

        self.behaviour_timer_ = self.create_timer(1.0, self.check_cb)
    def check_cb(self):
        req = False
        if self.loc_flag and self.robot_flag:
            self.get_logger().info('Robot ready to initialise motors')
            req = True
        else:
            self.get_logger().warning('Robot not ready')

        request = SetBool.Request()
        request.data = req
        future = self.cli_.call_async(request)
        future.add_done_callback(self.server_future_callback)
    def server_future_callback(self, future):
        resp = future.result()
        self.get_logger().info(f'Server response: {resp.success}, w/ msg: {resp.message}')

    def loc_cb(self, msg: Bool):
        self.loc_flag = msg.data

    def robot_cb(self, msg: Bool):
        self.robot_flag = msg.data
def main(args=None):
    rclpy.init(args=args)
    node = RobotSafetyCtrl()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()
        

    