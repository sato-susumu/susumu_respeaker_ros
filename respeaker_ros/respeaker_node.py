import rclpy
from rclpy.qos import QoSProfile, QoSDurabilityPolicy
from rclpy.node import Node
from std_msgs.msg import  Int32
import math
import angles

from respeaker_ros.interface import RespeakerInterface

class RespeakerNode(Node):
    def __init__(self):
        super().__init__('respeaker_node')
        self.get_logger().info(f"Starting respeaker_node")

        #parameters
        self.doa_xy_offset = self.declare_parameter('doa_xy_offset', 0.0)
        self.doa_yaw_offset = self.declare_parameter('doa_yaw_offset', 90.0)

        self.respeaker = RespeakerInterface() #mic-array initialisation
        self.respeaker.write('AGCGAIN', 50.0)
        self.respeaker.write('AGCONOFF', 0)
        self.respeaker.write('CNIONOFF', 0)
        self.respeaker.write('GAMMA_NS_SR', 1.8)
        self.respeaker.write('MIN_NS_SR', 0.01)
        self.respeaker.write('STATNOISEONOFF_SR', 1)


        self.timer = self.create_timer(0.1, self.timer_callback)

        self.prev_doa = None
        latching_qos = QoSProfile(depth=1,
            durability=QoSDurabilityPolicy.TRANSIENT_LOCAL)
        
        self._pub_doa_raw = self.create_publisher(Int32, 'doa_raw', latching_qos) #degree of audio

        self.get_logger().info(f"Started respeaker_node")

    def timer_callback(self):
        doa_rad = math.radians(self.respeaker.direction - 180.0)
        doa_rad = angles.shortest_angular_distance(
            doa_rad, math.radians(self.doa_yaw_offset.value))
        doa = math.degrees(doa_rad)

        # doa
        if doa != self.prev_doa:
            self._pub_doa_raw.publish(Int32(data=int(doa)))
            self.prev_doa = doa


def main(args=None):
    rclpy.init(args=args)

    audio_publisher = RespeakerNode()

    try:
        rclpy.spin(audio_publisher)
    except KeyboardInterrupt:
        pass

    audio_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
