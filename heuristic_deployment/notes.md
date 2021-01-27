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

> Suggestion: Straight line path following with obstacle avoidance



## Exploring

When in the exploring stage, the "new" min should fly in a direction not previously explored. It should also 

## Terminating (landing)