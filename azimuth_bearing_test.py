import matplotlib.pyplot as plt
from matplotlib.patches import Arc

import numpy as np

if __name__ == "__main__":

  ### Position of sensor 0
  s_0 = np.zeros(2, )

  ### Distance and angle from sensor to target (angle counter-clockwise relative x-axis (East))
  r = 1
  thetas = np.linspace(0, 2*np.pi, 8)

  for theta in thetas:

    ### Position of target
    p = r*np.array([np.cos(theta), np.sin(theta)])
    ans = np.rad2deg(np.mod(theta - np.pi/2, 2*np.pi))

    azimuth_bearing_p_s_0 = np.mod(-np.arctan2(p[0]-s_0[0], p[1]-s_0[1]), 2*np.pi)
    print(np.rad2deg(azimuth_bearing_p_s_0), ans)
    radius = np.linalg.norm(s_0-p)

    ### Creating figure and axis
    fig, ax = plt.subplots()

    ### Plotting points
    ax.scatter(*p)
    ax.annotate("$p$", xy = (p[0], p[1]), fontsize=14)
    ax.scatter(*s_0)
    ax.annotate("$s_{0}$", xy = (s_0[0], s_0[1]), fontsize=14)

    ### Plotting line from s_0 with calculated azimuth
    tmp = s_0 + radius*np.array([np.cos(np.pi/2 + azimuth_bearing_p_s_0), np.sin(np.pi/2 + azimuth_bearing_p_s_0)])
    ax.plot([s_0[0], tmp[0]], [s_0[1], tmp[1]], color="red")

    ### Plotting North-axis
    ax.plot([s_0[0], s_0[0]], [s_0[1], s_0[1] + 1], color="black", linestyle="dashed")
    
    ### Plotting angle arc
    arc = Arc(s_0, .5, .5, 0, 90, np.rad2deg(azimuth_bearing_p_s_0) + 90)
    ax.add_patch(arc)

    ### Adjusting axis and showing figure
    ax.axis("equal")
    plt.show()
