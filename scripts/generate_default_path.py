#!/usr/bin/env python
import yaml
import rospkg
import math
import numpy as np
import os
import copy


def generate_circle(r, cx, cy, delta_s, phi_0, height):
    delta_phi = float(delta_s) / r
    phis = np.arange(phi_0, phi_0 + 2 * math.pi, delta_phi, dtype=np.float)
    circle = []
    for phi in phis:
        x = math.cos(phi) * r + cx
        y = math.sin(phi) * r + cy
        z = height
        point = dict(x=x, y=y, z=z)
        circle.append(point)
    return circle


def main():
    circle = generate_circle(0.5, 1.0, 2.0, 0.01, 0, -0.5)
    start_position = copy.deepcopy(circle[0])
    output = dict(start_position=start_position, path=circle, loop=True)
    path = rospkg.RosPack().get_path("gantry_control")
    file_name = os.path.join(path, "default_path.yaml")
    with open(file_name, "w") as f:
        yaml.safe_dump(output, f)
    print("File written to '{}'".format(file_name))


if __name__ == "__main__":
    main()
