import matplotlib.pyplot as plt
import numpy as np
def xi(x_n_plus_one, x_is):
    return np.exp(-np.abs(x_n_plus_one - x_is))

def potential_1(x_n_plus_one, x_is, k_is):
    return (1/2)*np.sum(k_is*np.abs(x_n_plus_one - x_is - 0*xi(x_n_plus_one, x_is))**2)

def potential_2(x_n_plus_one, x_is, k_is):
    return (1/2)*np.abs(x_n_plus_one - np.sum(xi(x_n_plus_one, x_is)*x_is))**2

if __name__ == "__main__":
    fig, ax = plt.subplots()
    x_0 = np.array([0])
    x_1 = np.array([3])
    
    x_is = np.concatenate((x_0, x_1), axis=0)

    x_n_plus_one = np.linspace(-6, 6, 1000)
    k_is = np.ones((2, ))
    pot1 = np.array([potential_1(x_n_plus_one[i], x_is, k_is) for i in np.arange(x_n_plus_one.shape[0])])
    pot2 = np.array([potential_2(x_n_plus_one[i], x_is, k_is) for i in np.arange(x_n_plus_one.shape[0])])
    ax.plot(x_n_plus_one, pot1, color="green")
    ax.plot(x_n_plus_one, pot2, color="red")

    ax.scatter(x_is, np.zeros(x_is.shape))

    plt.grid()
    plt.show()
