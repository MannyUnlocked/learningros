import rclpy
from rclpy.node import Node
from std_srvs.srv import SetBool

class MotorSafetyControl(Node):
    '''Service server node representing a motor enable relay'''
 
    def __init__(self):
        super().__init__('motor_safety_control')
 
        self.srv_ = self.create_service(
            SetBool,
            'motor_sft_ctrl',
            self.motor_relay_ctrl,
        )
        self.get_logger().info('Node started successfully')

    def motor_relay_ctrl(self, request: SetBool.Request, response: SetBool.Response):
        req = request.data
        log_message = 'Activating motor' if req else 'Activation failed'
        self.get_logger().info(f'{req}')

        response.success = True
        response.message= log_message
 
        return response

def main(args=None):
    rclpy.init(args=args)
    node= MotorSafetyControl()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()


