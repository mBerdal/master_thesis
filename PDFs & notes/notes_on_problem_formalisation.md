# Notes on problem formalisation

> **Problem 2**: Consider agents that can move only linearly. They have to self-deploy one-by-one along a line, with no obstacles. The deploying drone must always go beyond the previously deployed one, but must not move too far in order to maintain connectivity.

### Two drone case
Consider a drone $\nu_{1}$ already deployed and is now placed at $x_{1}\in\mathbb{R}$. $\nu_{1}$ is connected to all other drones within the interval $[x_{1} - \delta, x_{1} + \delta]$. The new drone, $\nu_{2}$ should deploy itself and land at some location $x_{1} < x_{2}^{*} < x_{1} + \delta$, i.e. move beyond $\nu_{1}$, but be connected with $\nu_{1}$.

The potential between $\nu_{1}$ and $\nu_{2}$ is modelled a
$$
U(x_{1}, x_{2}) = \frac{1}{2}\kappa d(x_{1}, x_{2})^{2},\quad\text{where}\quad\kappa\in\mathbb{R}_{+}.
$$
The distance measure, $d(x_{1}, x_{2})$, between $\nu_{1}$ and $\nu_{2}$ is modelled as:
$$
d(x_{1}, x_{2}) = ||x_{1}-x_{2}+\xi(\text{RSSI})||,
$$
where $\xi(\text{RSSI})>0$ is a value proportional to the $\text{RSSI}$ signal between $\nu_{1}$ and $\nu_{2}$.

The potential energy, $U(x_{1}, x_{1})$ is minimized when $d(x_{1}, x_{2}) = 0$.
$$
d(x_{1}, x_{2}) = 0 \implies x_{1}-x_{2}+\xi(\text{RSSI}) = 0
$$
Now, since $\xi(\text{RSSI}) > 0$ we have:
$$
x_{1} - x_{2} < x_{1} - x_{2} + \xi(\text{RSSI}) = 0 \implies x_{2} > x_{1}
$$
Thus the potential energy between $\nu_{1}$ and $\nu_{2}$ is minimized for some $x_{2} > x_{1}$.

### Extended case
$$
U(x_{1}\dots x_{n+1}) = \frac{1}{2}\sum\limits_{i=1}^{n}\kappa_{i}||x_{i} - x_{n+1} + \xi(d_{(n+1)i})||^{2},
$$
where $d_{ij} = ||x_{i} - x_{j}||$ is the distance between $\nu_{i}$ and $\nu_{j}$, and $\nu_{n+1}$ should be placed so as to minimize $U(\cdot)$.

$\xi(d_{ij})$ is modelled as a sigmoid function such that:
$$
\xi(d_{ij}) = \begin{cases}
    0,&d_{ij} > \bar{d}\\
    \bar{\xi},&d_{ij} = 0
\end{cases}
$$
A function approximating this is:
$$
\tilde{\xi}(d_{ij}) =
    2\bar{\xi}(1-\frac{1}{1+e^{-kd_{ij}}}),\quad\text{where}\quad k=\frac{\ln(2\bar{\xi}-\tau)-\ln(\tau)}{\bar{d}},\;\tau < \bar{\xi},
$$
which can be rewritten as
$$
\tilde{\xi}(d_{ij}) = 2\bar{\xi}\Bigg(1-\frac{1}{1+\big(2\frac{\bar{\xi}}{\tau}-1\big)^{-\frac{d_{ij}}{\bar{d}}}}\Bigg)
$$
Defining $\alpha:=2\frac{\bar{\xi}}{\tau}-1$ yields:
$$
\tilde{\xi}(d_{ij}) = 2\bar{\xi}\Bigg(1-\frac{1}{1+\alpha^{-\frac{d_{ij}}{\bar{d}}}}\Bigg)
$$
>$\tilde{\xi}(\cdot)$ has the following properties:
>
> 1. $\tilde{\xi}(0) = \bar{\xi}$
> 2. $\tilde{\xi}(d_{ij}) < \tau\;\forall\;d_{ij} > \bar{d}$

## Where is the equilibrium of $U(\cdot)$ wrt. $x_{n+1}$?



