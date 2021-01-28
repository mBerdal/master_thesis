# Heuristic deployment notes
## Following

When deploying a new MIN, it should travel into the environment towards some previously deployed MIN, called the target. When the deployed MIN has arrived at the target, it should start exploration.
### What previously MIN should become the target?
It is desirable that, during the exploration phase, the new  MIN should travel into space not previously explored. Due to this, it is desirable that the new MIN is close to the frontier of the explored area when starting exploration.

Assuming that the previously deployed MIN is at the frontier of the explored area (which it must be if it was succesfull in its exploration phase), it should be the target.

Alternatively the MIN which resides at the frontier of the explored area with the fewest neighbors could be the target. Odds are that the MIN with fewest neighbours lie at the frontier. Hence the frontier check could be disregarded, and the MIN with fewest neighbors could be chosen to be the target. If more than one MIN have the same amount of neighbors, choose the one that is closest to the SCS.

> Q1: how to define the frontier of the explored area?
>
> A1: Any MIN whose communication disk is not fully covered by those of other MINs is the the frontier (not computationally feasible, and not robust when using position estimates to decide). Some other criteria should be found.
### How should the new MIN decide it's path to the target?
Assuming the SCS stores the directed graph, $\mathcal{G}$, where MINs are nodes. MINs $i$ and $j$ have an edge, $e_{ij}$, from $i$ to $j$ if $i$ was the target of $j$. Performing a DFS starting from the SCS and finding the target (defined in one of the ways described above) for the MIN that is to be deployed yields a sequence of MINs which can be visited when travelling from the SCS to the target.

The DFS returns an ordered sequence $\mathcal{S} = \{SCS\dots\ t\}$ of MINs (and the SCS) that can be visited when travelling from the SCS to the target. We define $b_{0} = SCS$ and $b_{|\mathcal{S}|-1} = t$. For all MINs, $b_{i}\in\mathcal{S},1\leq i<|\mathcal{S}|$, it started its exploration phase at $\hat{\mathbf{x}}_{b_{i-1}}$ and ended its exploration phase at $\hat{\mathbf{x}}_{b_{i}}$. Thus we know that there is a feasible path from MIN $b_{i-1}$ to $b_{i}$ for all $1\leq i<|\mathcal{S}|$.

If there is a feasible path from $b_{i-1}$ to $b_{i}$ for all $1\leq i<|\mathcal{S}|$, we can connect these paths to find a feasible path from $b_{0} = SCS$ to $b_{|\mathcal{S}|-1}=t$.

> Suggestion: Straight line path following (SLPF) with obstacle avoidance
> 
> If previously deployed MINs collect information about the environment (iteratively creates an occupancy grid), one could find the shortest path from the SCS to the target which is entirely contained within the free cells of the occupancy grid, and have the new MIN follow this path towards the target.



## Exploring

When in the exploring stage, the "new" MIN should fly in a direction not previously explored. Regardless of the direction the new MIN should avoid obstacles.

> ### MIN
> A MIN $i$ is described by its position $\mathbf{x}_{i}^{i}$ in the intertial frame, and its rotation about the intertial z-axis, $\psi_{i}$.

> #### Range sensors
> Each MIN is equipped with 4 range sensors, $r_{i},\;i\in[0,4)$. Sensor $r_{i}$ is mounted on the body at an angle $\theta_{i} = 90^{\circ}\cdot i$. The range sensors can maximally detect objects at a distance $d_{max}$ away. 
> Given the description of an obstacle $\mathcal{O}=\{\mathbf{x}^{i}: f(\mathbf{x}^{i})\leq 0\}$ in the inertial frame and a MIN positioned at $\mathbf{x}_{i}^{i}$ in the inertial frame with a yaw angle $\psi_{i}$. A range sensor, $r_{j}$ is mounted on the MIN at an angle $\theta_{j}$. The set 
$$\mathcal{R}_{j} = \{d: \mathbf{x}_{i}^{i} + \mathbf{R}_{z}(\psi_{i})\mathbf{R}_{z}(\theta_{i})\begin{bmatrix}
    d\\ 0
\end{bmatrix}\in\partial\mathcal{O}, 0\leq d\leq d_{max}\}$$
>Is the set of all points along the sensor $r_{j}$'s x-axis that intersects with the boundary of the obstacle $\mathcal{O}$. When polling a range sensor, it returns measurements according to:
$$
m_{j} = \begin{cases}
    \min\mathcal{R}_{j}, &\mathcal{R}_{j}\neq\emptyset\\
    \infty, &\text{otherwise}
\end{cases}
$$
### Currently implemented approach

1. Compute nominal exploration direction (rotation about the inertial z-axis) according to:
   $$
   \psi_{nom} = \frac{\sum\limits_{j\in N(i)}\alpha_{j}\psi_{ij}}{\sum\limits_{j\in N(i)}\alpha_{j}},\quad\text{where}\quad\alpha_{j} = \begin{cases}
       1, &N(j) < \kappa\\
       0, &\text{otherwise}
   \end{cases}
   $$
2.  Using the range sensors, $r_{j},j\in[0, 4)$, an obstacle avoidance vector is calculated:
$$
\mathbf{o}^{i} = \sum\limits_{\{r_{j}: m_{j} < \infty\}}-\bigg(1-\frac{m_{j}}{d_{max}}\bigg)\begin{bmatrix}
    \cos(\psi_{i} + \theta_{j})\\
    \sin(\psi_{i} + \theta_{j})
\end{bmatrix} = \begin{bmatrix}
    o_{x}\\ o_{y}
\end{bmatrix}
$$
> #### Note
> When a range sensor $r_{j}$ detects a n obstacle a distance $d_{max}$ away, we want $r_{j}$ to have zero contribution to the obstacle avoidance vector. When a sensor senses an obstacle $0$ meters away, we want it to dominate the obstacle avoidance vector. This is the reason behind the scaling term $1-\frac{m_{j}}{d_{max}}$.

3. Compute an overall yaw angle according to:
$$
\psi_{eff} = \text{arctan2}\big(\sin(\psi_{nom}) + o_{y}, \cos(\psi_{nom}) + o_{x}\big)$$
## Terminating (landing)