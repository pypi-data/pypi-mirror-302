import sys
import os
import numpy as np


import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from ....utils import bmutils

class mechanism33(bmutils):
    def __init__(self, settings):
        self.settings = settings
        self.fig, self.ax = plt.subplots(figsize=(10, 6))
        self.ani = None

        # Extract parameters from settings
        self.start_theta = settings['start_theta']
        self.radius = settings['radius']
        self.instances = settings['instances']
        self.forward_stroke_angle = settings['forward_stroke_angle']
        self.stroke_length = settings['stroke_length']
        # self.b = settings['b']

        # Initialize plot elements
        self.point_line = [] # = self.ax.plot([], [], color='green', linestyle='-', linewidth=2, label='Line to Point A')
        self.point_dot = [] # self.ax.scatter([], [], color='red', zorder=5)
        self.center_dot = self.ax.scatter([0], [0], color='red', zorder=5)  # Fixed here (no need to unpack)
        # self.pointB_dot = self.ax.scatter([], [], color='red', zorder=5)
        # self.point_label = self.ax.text(0, 0, 'A', fontsize=12, ha='right', color='red')

        self.cam_profile_line = []
        self.return_line = []
        for instance in self.instances:
            point_line, = self.ax.plot([], [], color=instance["color"], linestyle='-', linewidth=2, label='Crank')
            point_dot = self.ax.scatter([], [], color=instance["color"], zorder=5)

            self.point_dot.append(point_dot)
            self.point_line.append(point_line)
            cam_profile_line, = self.ax.plot([], [], color=instance["color"], linestyle='-', linewidth=2)
            return_line, = self.ax.plot([], [], color=instance["color"], linestyle='-', linewidth=2)
            self.cam_profile_line.append(cam_profile_line)
            self.return_line.append(return_line)

        self.setup_plot()

    def setup_plot(self):
        self.ax.set_title("Mechanism 33")
        self.ax.set_aspect('equal')
        self.ax.grid(True)
        self.ax.axis("off")
        radius = self.radius
        self.ax.set_xlim(-2 * radius, 2 * radius)
        self.ax.set_ylim(-1.2 * radius, 1.2 * radius)
        self.follower_circle()
        super().watermark(self.ax)

    def follower_circle(self):
        theta_circle = np.linspace(0, 2*np.pi, 1000)
        x_circle = self.radius * np.cos(theta_circle)
        y_circle = self.radius * np.sin(theta_circle)
        self.ax.plot(x_circle, y_circle, label='Circle', color='blue')

    def get_cam_profile(self, theta, d_theta):
        start_theta = self.start_theta
        displacement_per_theta = self.stroke_length / self.forward_stroke_angle
        d_theta = d_theta % (2*np.pi)

        theta_rad = np.linspace(start_theta, start_theta + np.deg2rad(self.forward_stroke_angle), 1000)
        x, y = self.radius * np.cos(theta_rad), self.radius * np.sin(theta_rad)

        d_theta_profile = np.rad2deg(theta_rad - start_theta)

        point_x =       self.radius * np.cos(theta)
        x_for_profile = point_x + (np.rad2deg(d_theta)) * displacement_per_theta

        x_diff = x_for_profile - point_x         
        
        if 0 <= d_theta and d_theta <= np.deg2rad(self.forward_stroke_angle):
            x_profile_displaced = (x + d_theta_profile * displacement_per_theta - x_diff)
        else:
            x_profile_displaced = (x + d_theta_profile * displacement_per_theta)
            x1, x2 = x_profile_displaced[0], x_profile_displaced[-1]
            y1, y2 = y[0], y[-1]
            m = (y2 - y1) / (x2 - x1)
            b = y1 - m * x1
            y_target = self.radius * np.sin(theta)
            x_for_y = (y_target - b) / m
            x_diff = x_for_y - point_x
            x_profile_displaced = (x + d_theta_profile * displacement_per_theta - x_diff)
   
        return x_profile_displaced, y


    def plot(self, d_theta=0):
        theta = self.start_theta + d_theta
        for i, instance in enumerate(self.instances):
            instance_theta = theta + np.deg2rad(instance["offset"])
            instance_d_theta = d_theta + np.deg2rad(instance["offset"])
            point_x = self.radius * np.cos(instance_theta)
            point_y = self.radius * np.sin(instance_theta)
            x_profile_displaced, y = self.get_cam_profile(instance_theta, instance_d_theta)
            self.cam_profile_line[i].set_data(x_profile_displaced, y)
            self.return_line[i].set_data([x_profile_displaced[0], x_profile_displaced[-1]], [y[0], y[-1]])
            self.point_line[i].set_data([0, point_x], [0, point_y])
            self.point_dot[i].set_offsets([point_x, point_y])

        return self

    def update(self, interval=50, frames=100):
        speed = self.settings.get("speed", 1)
        animation_rounds = self.settings.get("animation_rounds", 1)
        total_angle = 2*np.pi * animation_rounds
        displacements = np.linspace(0, total_angle, int(frames/speed))

        def animate(displacement):
            self.plot(displacement)

        self.ani = FuncAnimation(self.fig, lambda displacement: animate(displacement),
                                 frames=displacements, interval=interval, repeat=True)
        return self

    @staticmethod
    def Settings(radius=1, forward_stroke_angle=250, speed=1, animation_rounds=1, num_instances = 2, stroke_length=1.2, start_theta=-160):

        colors = [
           "black","orange", "green", "gray"
        ]
        instances = [{"color":colors[i%len(colors)], "offset": 360/num_instances *( i+0)} for i in range(num_instances)]
        return {
            "radius": radius,
            "forward_stroke_angle": forward_stroke_angle,
            "stroke_length": stroke_length,
            # "b": b,
            "speed": speed,
            "animation_rounds": animation_rounds,
            "instances": instances,
            "start_theta": np.deg2rad(start_theta)#-np.pi/2
        }

    @staticmethod
    def info():
        return (
            "Mechanism Description:\n"
            "-----------------------\n"
            "A variation of scotch-yoke with constant speed in forward stroke and quickreturn.\n"
            "**Applications**:\n"
            "Clamp-on long range linear motion mechanisms and walking mechanisms\n"
            "**Notes**:\n"
            "You may need to select values for stroke_length, start_theta and  forward_stroke_angle for which the cam profile will not cross the shaft axis in the case where multiple co-axial cams are used\n"
        )