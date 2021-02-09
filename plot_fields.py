import matplotlib.pyplot as plt
import numpy as np
def xi(x_n_plus_one, x_is):
    return np.exp(-np.abs(x_n_plus_one - x_is))

def potential_1(x_n_plus_one, x_is, k_is):
    return (1/2)*np.sum(k_is*np.abs(x_n_plus_one - x_is - 0*xi(x_n_plus_one, x_is))**2)

def potential_2(x_n_plus_one, x_is, k_is):
    return (1/2)*np.abs(x_n_plus_one - np.sum(xi(x_n_plus_one, x_is)*x_is))**2

def potential_3(x_n_plus_one, x_is, k_is):
    """Covariance-based potential

    Args:
        x_n_plus_one ([type]): [description]
        x_is ([type]): [description]
        k_is ([type]): [description]
    """

    n = x_is.shape[1]
    x_bar = (x_n_plus_one + np.sum(x_is, axis=1).reshape(2, 1))
    X = np.concatenate((x_is, x_n_plus_one), axis=1)
    diffs = (X-x_bar)
    s = np.zeros((2, 2))
    for i in np.arange(diffs.shape[1]):
        d = diffs[:, i].reshape(2, 1)
        s += d@d.T
    return (1/n**2)*np.linalg.det(s)


if __name__ == "__main__":
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    x_0 = np.array([0, 0]).reshape(2, 1)
    x_1 = np.array([3, 0]).reshape(2, 1)
    x_2 = np.array([3, 3]).reshape(2, 1)
    
    x_is = np.concatenate((x_0, x_1, x_2), axis=1)
    """
    x_n_plus_one = np.linspace(-6, 6, 1000)
    k_is = np.ones((2, ))
    pot1 = np.array([potential_1(x_n_plus_one[i], x_is, k_is) for i in np.arange(x_n_plus_one.shape[0])])
    pot2 = np.array([potential_2(x_n_plus_one[i], x_is, k_is) for i in np.arange(x_n_plus_one.shape[0])])
    ax.plot(x_n_plus_one, pot1, color="green")
    ax.plot(x_n_plus_one, pot2, color="red")

    ax.scatter(x_is, np.zeros(x_is.shape))
    """
    dx, dy = 0.1, 0.1
    X = np.arange(-10, 10, dx)
    Y = np.arange(-10, 10, dy)
    XX, YY = np.meshgrid(X, Y)
    mesh = np.zeros(XX.shape)
    for i in np.arange(X.shape[0]):
        for j in np.arange(Y.shape[0]):
            x = X[i]
            y = Y[j]
            mesh[j, i] = potential_3(np.array([x, y]).reshape(2, 1), x_is, None)

    surf = ax.plot_surface(
        XX,
        YY,
        mesh
        )
    ax.scatter(*x_is, color="orange")
    plt.show()
