#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import sys
import os
from PIL import Image
from custom_messages.msg import ImagePiece
import subprocess

class ImagePieceSubscriber(Node):
    def __init__(self, piece_id):
        super().__init__(f'image_piece_subscriber_{piece_id}')
        self.piece_id = piece_id
        self.bridge = CvBridge()
	# Subscribe to the topic that contains all the pictures
        self.subscription = self.create_subscription(
            ImagePiece,
            'image_pieces',
            self.listener_callback,
            10
        )
        self.subscription

    def show_image(self, img_path):
        # Create a sub-process that shows the received image with the fbi-function
        subprocess.run(["fbi", "--noverbose","-a", f"{img_path}"])

    def listener_callback(self, msg):
        self.get_logger().info('I heard: "%d"' % msg.piece_id)

        if msg.piece_id == self.piece_id:
            self.get_logger().info('I listened only "%d"' % msg.piece_id)
            # Convert ROS Image message to OpenCV image
            cv_image = self.bridge.imgmsg_to_cv2(msg.image, desired_encoding='bgr8')
            # cv2.imshow(f"Image Piece", cv_image)
            img_path = '/home/rlab/received_images/piece.png'
            cv2.imwrite(img_path, cv_image)

            self.show_image(img_path)
            self.get_logger().info("Received image piece.")


def main(args=None):
    rclpy.init(args=args)
    if len(sys.argv) < 2:
        print("Usage: image_piece_subscriber.py <piece_id>")
        sys.exit(1)

    try:
        piece_id = int(sys.argv[1])
    except ValueError:
        print("Piece ID must be an integer.")
        sys.exit(1)

    node = ImagePieceSubscriber(piece_id)
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
