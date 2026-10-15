import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from moveit_msgs.action import MoveGroup
from moveit_msgs.msg import MotionPlanRequest, Constraints, JointConstraint, PositionConstraint, OrientationConstraint
from shape_msgs.msg import SolidPrimitive
from geometry_msgs.msg import PoseStamped, Quaternion

#Creating the class for the MoveIt Action Client and creating the action client for the MoveIt Action Server.
class RX200MoveItActionClient(Node):
    def __init__(self):
        super().__init__('rx200_moveit_control')
        self.get_logger().info('RX200 MoveIt Action Client has been initialized.')

        self._cli = ActionClient(self, MoveGroup, '/move_action')
        while not self._cli.wait_for_server(timeout_sec=1.0):
            self.get_logger().warning('[WARNING] Action server not up')
        self.arm_group = 'interbotix_arm'
        self.gripper_group = 'interbotix_gripper'
        self.ee_link = 'rx200/ee_gripper_link'
        self.base_link = 'rx200/base_link'
        self.gripper_joint = 'left_finger' #note we changed this in sim, confirm for real robot

        self.declare_parameter('gripper_start_state', value=True)
        self.send_gr_pose(self.get_parameter('gripper_start_state').value)

        self.get_logger().info('Robot Initialized')

    def send_ee_pose(self, x, y, z, w=1.0):
        P = PoseStamped()
        P.header.frame_id = self.base_link
        P.pose.position.x = x
        P.pose.position.y = y
        P.pose.position.z = z
        P.pose.orientation = Quaternion(x=0.0, y=0.7071, z=0.0, w=0.7071) #FIXME
        # order form for arm
        req = MotionPlanRequest()
        req.group_name = self.arm_group
        req.allowed_planning_time = 5.0
        req.num_planning_attempts = 3   
      # position constraints
        pc = PositionConstraint()
        pc.header.frame_id = self.base_link
        pc.link_name = self.ee_link
        sp = SolidPrimitive()
        sp.type = SolidPrimitive.SPHERE
        sp.dimensions = [0.01]
        pc.constraint_region.primitives = [sp]
        pc.constraint_region.primitive_poses = [P.pose]
        pc.weight = 1.0
        # orientation constraints
        oc = OrientationConstraint()
        oc.header.frame_id = self.base_link
        oc.link_name = self.ee_link
        oc.orientation = P.pose.orientation
        oc.absolute_x_axis_tolerance = 0.05
        oc.absolute_y_axis_tolerance = 0.05
        oc.absolute_z_axis_tolerance = 0.05
        oc.weight = 1.0

        #bundle wrap and send the goal to the MoveIt Action Server for the end effector to move to the desired pose.
        gc = Constraints()
        gc.position_constraints = [pc]
        gc.orientation_constraints = [oc]
        req.goal_constraints = [gc]

        goal = MoveGroup.Goal()
        goal.request = req
        goal.planning_options.plan_only = False
        goal.planning_options.replan = True
        goal.planning_options.look_around = False

        future = self._cli.send_goal_async(goal, self._feedback_cb)
        future.add_done_callback(self._goal_response_cb)
        future = self._cli.send_goal_async(goal, self._feedback_cb)
        future.add_done_callback(self._goal_response_cb)
#defining constaints and sending the goal to the MoveIt Action Server for the gripper to open or close.
    def send_gr_pose(self, open=True):
        req = MotionPlanRequest()
        req.group_name = self.gripper_group
        req.allowed_planning_time = 2.0
        req.num_planning_attempts = 1

        jc = JointConstraint()
        jc.joint_name = self.gripper_joint
        jc.position = 0.035 if open else 0.017   #note we changed this in sim, confirm for real robot
        jc.tolerance_above = 0.001
        jc.tolerance_below = 0.001
        jc.weight = 1.0

        gc = Constraints()
        gc.joint_constraints = [jc]
        req.goal_constraints = [gc]

        goal = MoveGroup.Goal()
        goal.request = req
        goal.planning_options.plan_only = False

        future = self._cli.send_goal_async(goal)
        future.add_done_callback(self._goal_response_cb)
    def _goal_response_cb(self, future):
        handle_goal = future.result()
        if not handle_goal.accepted:
            self.get_logger().error('[ERROR] Goal was not accepted by the action server.')
            return
        self.get_logger().info('[INFO] Goal accepted by the action server.')
        handle_goal.get_result_async().add_done_callback(self._result_cb)
    def _result_cb(self, future):
        result = future.result().result
        code = result.error_code.val
        self.get_logger().info(f'[INFO] Result code: {code}')
    def _feedback_cb(self, feedback_msg):
        state = feedback_msg.feedback.state
        self.get_logger().info(f'[INFO] Current state:: {state}')
def main(args=None):
    rclpy.init(args=args)
    node = RX200MoveItActionClient()
    node.send_ee_pose(0.7, 0.0, 0.5)
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()