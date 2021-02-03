from scipy.optimize import fmin_ncg
import numpy as np
import matplotlib.pyplot as plt
from numbers import Number

"""
  Base functions
""" 
def f_1(Phi):
  return np.sum(np.sin(Phi), axis=0)

def f_2(Phi):
  return f_1(2*Phi)

def f_3(Phi):
  return np.sum(np.cos(Phi), axis=0)

def f_4(Phi):
  return f_3(2*Phi)

"""
  Objective function
"""
def f(Phi):
  return f_1(Phi)**2 + f_2(Phi)**2 + f_3(Phi)**2 + f_4(Phi)**2

"""
  Gradient of objective function
"""
def fprime(Phi):
  temp = 2*np.column_stack((np.cos(Phi), 2*np.cos(2*Phi), -np.sin(Phi), -2*np.sin(2*Phi)))
  return temp@np.array([f_1(Phi), f_2(Phi), f_3(Phi), f_4(Phi)])

"""
  Hessian of objective function
"""
def fhess(Phi):
  diffs = Phi[np.newaxis].T-Phi
  off_diag = 2*(np.cos(diffs) + 4*np.cos(2*diffs))
  diag = np.diag(
    2*(1 - f_1(Phi)*np.sin(Phi) - f_3(Phi)*np.cos(Phi) + 4*(1 - f_2(Phi)*np.sin(2*Phi) - f_4(Phi)*np.cos(2*Phi)))
  )
  return diag + off_diag

"""
  Fisher information matrix determinant
"""
def fisher_det(Phi, sigma):
  N = Phi.shape[0]
  f1, f2 = f_1(Phi), f_2(Phi)
  f3, f4 = f_3(Phi), f_4(Phi)
  return (1/np.power(sigma, 6))*(\
    np.power(N, 3)/4\
   -(N/4)*np.power(f4, 2)\
   -(N/2)*(\
     np.power(f3, 2) + np.power(f1, 2)
    )\
   -f2*(\
      (N/4)*f2 - f3*f1
    )\
   -(1/2)*f4*(\
      np.power(f1, 2) - np.power(f3, 2)
    )
  )

"""
  Azimuth bearing from sensors to a point
  :param S: Array of sensor (x, y) coords.
  :param px: x coords. of points 
  :param py: y coords. of points 
  :return: matrix of azimuth bearings of shape (n_sensors, n_y_coords, n_x_coords)
"""
def get_azimuth_bearing(S, px, py):
  if isinstance(px, Number):
    px = np.array([[px]])
  if isinstance(py, Number):
    py = np.array([[py]])
  temp = np.repeat(np.repeat(S[:, :, np.newaxis], px.shape[0], axis=2)[:, :, :, np.newaxis], py.shape[1], axis=3)
  temp_px = np.repeat(px[np.newaxis], S.shape[1], axis=0)
  temp_py = np.repeat(py[np.newaxis], S.shape[1], axis=0)
  return np.mod(-np.arctan2(temp_px-temp[0], temp_py-temp[1]), 2*np.pi)

"""
  Function for plotting configuration
  :param ax: axis to plot on
  :param p: Position of target
  :param S: Position of anchors
"""
def plot_configuration(ax, p, S):
  if not p is None:
    ax.scatter(*p, color="red")
    ax.annotate("$p$", xy=(p[0], p[1]), fontsize=14)
  ax.scatter(*S, color="blue")
  for i in np.arange(S.shape[1]):
    ax.annotate(f"${i}$", xy=(S[0, i], S[1, i]), fontsize=14)

def plot_color_map(fig, ax, res, bounds_x, bounds_y, S, sigma = 1, p = None):
  xs = np.linspace(*bounds_x, res)
  ys = np.linspace(*bounds_y, res)
  XX, YY = np.meshgrid(xs, ys)

  zs = fisher_det(get_azimuth_bearing(S, XX, YY), sigma)
  c = ax.pcolormesh(xs, ys, zs, cmap='RdBu', vmin=zs.min(), vmax=zs.max(), shading="auto")
  ax.set_title("Fisher determinant")
  ax.axis([xs.min(), xs.max(), ys.min(), ys.max()])
  fig.colorbar(c, ax=ax)

  plot_configuration(ax, p, S)

if __name__ == "__main__":
  ### Number of sensors
  N = 3
  
  ### Initial positions of sensors
  S0 = np.random.uniform(-3, 3, 2*N).reshape(2, N)


  ### Position of target
  p = np.zeros(2, )

  cmap_fig1, cmap_ax1 = plt.subplots()
  plot_color_map(cmap_fig1, cmap_ax1, 1000, [-5, 5], [-5, 5], S0, 1, p)
  ### Azimuth bearing of all sensors
  Phi = get_azimuth_bearing(S0, p[0], p[1])
  
  ### Finding optimal azimuth bearing angles
  sol = fmin_ncg(f, Phi, fprime, fhess=fhess)

  ### Converting azimuth bearing to (x, y)-coordinates
  S = p[np.newaxis].T +  3*np.array([
    np.cos(sol),
    np.sin(sol)
  ])

  ### Plotting Fisher determinant value
  print(S.shape)
  cmap_fig, cmap_ax = plt.subplots()
  plot_color_map(cmap_fig, cmap_ax, 1000, [-5, 5], [-5, 5], S, 1, p)
  
  plt.show()