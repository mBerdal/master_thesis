import numpy as np
import matplotlib.pyplot as plt
import timeit

def sample_mean(samples, weights=None, get_sum_weights=False):

    """Computes sample mean (multi-dim, weighted)

    Args:
        samples (ndarray): k-by-N matrix where
        columns correspond to a single sample vector

        weights (ndarray, optional): 1-by-N array of weights
        associated with each sample

        get_sum_weights (bool, optional): wether or not the
        sum of weights should be returned

    Returns:
        ndarray, (float): sample mean of shape k-by-1
        , (sum of weights if get_sum_weights is set to True)
    """

    return np.average(
        samples, axis=1, weights=weights, returned=get_sum_weights
    ).reshape(-1, 1)

def sample_covar_mat(samples, weights=None):
    """Computes sample covariance matrix

    Args:
        samples (ndarray): 2-by-N matrix where
        columns correspond to a single sample vector

    Returns:
        [ndarray]: N-by-N sample covariance matrix
    """
    N = samples.shape[1]

    assert weights is None or weights.shape[0] == N and np.sum(weights) == 1,\
        "must have as many weights as samples, and weights must sum up to 1"

    if weights is None:
        weights = np.ones((N, ))/N

    W = 1/(1 - np.sum(np.power(weights, 2)))
    wm = sample_mean(samples, np.tile(weights, (2, 1)))

    t_11 = np.sum(weights*(samples[0, :] - wm[0])**2)
    t_22 = np.sum(weights*(samples[1, :] - wm[1])**2)
    t_12 = np.sum(weights*(samples[0, :] - wm[0])*(samples[1, :] - wm[1]))

    return W*np.array([
        [t_11, t_12],
        [t_12, t_22]
    ])
    
def generalized_sample_variance(samples):
    return np.linalg.det(sample_covar_mat(samples))

def total_sample_variance(samples):
    return np.trace(sample_covar_mat(samples))




def get_F(beacon_x_is, x_N, weights=None):
    N = beacon_x_is.shape[1] + 1

    Q = sample_covar_mat(
        np.hstack((beacon_x_is, x_N)),
        weights=weights
    )
    return -2*N/(N-1)*np.array([
        [-Q[1, 1],  Q[0, 1]],
        [ Q[0, 1], -Q[0, 0]]
    ])@(np.sum(beacon_x_is, axis=1, keepdims=True) - N*x_N)

def simple_visualizer():
    good_bucket = []
    bad_bucket = []

    A = np.array([
        [0, 1],
        [0, 0]
    ])

    prev_var = total_sample_variance(A)
    for x in np.linspace(-10, 10, 100, endpoint=False):
        v = np.array([[x], [0]])
        var = total_sample_variance(np.hstack((A, v)))
        if var > prev_var:
            good_bucket.append(v)
        else:
            bad_bucket.append(v)

    plt.scatter(*A, zorder=100)

    for v in good_bucket:
        plt.scatter(*v, color="green")
    for v in bad_bucket:
        plt.scatter(*v, color="red")
    
    plt.show()

if __name__ == "__main__":

    simple_visualizer()
    exit(0)

    A = np.array([
        [-1.5, 0, 1.5],
        [0, 10, 0],
    ])

    h = 1e-4
    x = np.zeros((2, 1))

    weights = np.array([1, 10, 1, 1])
    weights = weights/np.sum(weights)

    for i in range(int(10e10)):
        F = get_F(A, x, weights)
        x += h*F
        if np.linalg.norm(F) < 1e-4:
            break

    plt.scatter(*A, color="blue")
    plt.scatter(*x, color="green")

    plt.show()

