#!/bin/bash/env python

import argparse
import numpy as np
import math
from numpy.linalg import inv
from numpy import linalg as LA
from os.path import basename, expanduser, isfile, join, splitext
import socket
from matplotlib import pyplot as plt
import time
from skimage import measure

import rospy
from sensor_msgs.msg import CompressedImage
from geometry_msgs.msg import PoseArray, Point, Pose, Quaternion

from duckietown_utils import d8_compressed_image_from_cv_image, logger, rgb_from_ros, yaml_load, get_duckiefleet_root
from duckietown_utils import get_base_name, load_camera_intrinsics, load_homography, load_map, rectify
from duckietown_utils import load_map, load_camera_intrinsics, load_homography, rectify

<<<<<<< HEAD

=======
>>>>>>> devel-saviors-fabio
class Avoider():
	'''class to avoid detected obstacles'''
	def __init__(self, robot_name=''):
		# Robot name
		self.robot_name = robot_name

<<<<<<< HEAD
		# Parameter definitions
		self.lWidthRobot = 140  # mm
		self.lWidthLane = 250  # mm

		# Control parameters
		self.yAvoidanceMargin = 20  # mm

	def avoid(self, obstacle_poses_on_track, d_current, theta):
		self.d_target = 0
		self.d_current = d_current
		self.theta = theta
		emergency_stop = 0
		if len(obstacle_poses_on_track.poses) == 1:
			# self.d_robot = self.d_current
			# self.theta = self.theta_current
			x_obstacle = obstacle_poses_on_track.poses[0].position.x * 1000 # mm
			y_obstacle = obstacle_poses_on_track.poses[0].position.y * 1000 # mm
			r_obstacle = obstacle_poses_on_track.poses[0].position.z * 1000 # mm
			global_pos_vec = self.coordinatetransform(x_obstacle, y_obstacle, -self.theta, self.d_current)
			# x_global = global_pos_vec[0]
			y_global = global_pos_vec[1]
=======
	# Parameter definitions
	self.lWidthRobot = 140  # mm
	self.lWidthLane = 250  # mm

	# Control parameters
	self.yAvoidanceMargin = 20  # mm

	def avoid(self, obstacle_poses_on_track, d_robot, theta):
		self.d_target = 0
		self.d_robot = d_robot
		self.theta = theta
		emergency_stop = 0
		if len(obstacle_poses_on_track) == 1:
			# self.d_robot = self.d_current
			# self.theta = self.theta_current
			x_obstacle = obstacle_poses_on_track[0].pose.x
			y_obstacle = obstacle_poses_on_track[0].pose.y
			r_obstacle = obstacle_poses_on_track[0].pose.z
			global_pos_vec = self.coordinatetransform(x_obstacle, y_obstacle, -self.theta, self.d_robot)
			# x_global = global_pos_vec[1]
			y_global = global_pos_vec[2]
>>>>>>> devel-saviors-fabio
			# Stop if there is no space
			if abs(y_global) + self.lWidthLane / 2 - r_obstacle < self.lWidthRobot + self.yAvoidanceMargin:
				print('Emergency Stop')
				emergency_stop = 1
			# React if possible
<<<<<<< HEAD
			self.d_target = (y_global - np.sign(y_global) * (self.lWidthRobot / 2 + self.yAvoidanceMargin + r_obstacle))/1000
		elif len(obstacle_poses_on_track.poses) > 1:
			print('Number of obstacles reaching avoid function too high')
			emergency_stop = 1
		targets = [self.d_target, emergency_stop]
		return targets

	def coordinatetransform(self, x_obstacle, y_obstacle, theta, d_current):
		self.theta = theta
		self.d_current = d_current
		self.x_obstacle = x_obstacle
		self.y_obstacle = y_obstacle
		vector_local = [self.x_obstacle, self.y_obstacle]
		rot_matrix = [[math.cos(self.theta), -math.sin(self.theta)],
		                       [math.sin(self.theta), math.cos(self.theta)]]
		vector_global = np.dot(rot_matrix, vector_local) + np.array([0, self.d_current])
		x_global = vector_global[0]
		y_global = vector_global[1]
=======
			self.d_target = y_global - np.sign(y_global) * (self.lWidthRobot / 2 + self.yAvoidanceMargin + r_obstacle)
		elif len(obstacle_poses_on_track) > 1:
			print('Number of obstacles reaching avoid function too high')
		targets = [self.d_target, emergency_stop]
		return targets

	def coordinatetransform(self, x_obstacle, y_obstacle, theta, d_robot):
		vector_local = np.array([x_obstacle, y_obstacle])
		rot_matrix = np.matrix([math.cos(theta), -math.sin(theta)], [math.sin(theta), math.cos(theta)])
		vector_global = rot_matrix * vector_local + np.array([0, d_robot])
		x_global = vector_global(1)
		y_global = vector_global(2)
>>>>>>> devel-saviors-fabio
		return np.array([x_global, y_global])
