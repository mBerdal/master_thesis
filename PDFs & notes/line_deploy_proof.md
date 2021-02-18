# Qualitative properties of $\xi$

$$
\begin{aligned}
  &\xi_{n+1, i} = f(||x_{n+1} - x_{i}||, \dots) =  f(d_{n+1, i}, \dots)\\
  &0 \leq \xi_{n+1, i} \leq \bar{\xi} \; \forall \; 1 \leq i \leq n\\

  &\frac{\partial}{\partial d_{n+1, i}} f(d_{n+1, i}, \dots) \leq 0\\
  &\frac{\partial}{\partial x_{n+1}} \xi_{n+1, i} = \frac{\partial}{\partial d_{n+1, i}} f(d_{n+1, i}, \dots)\cdot\frac{\partial}{\partial x_{n+1}}d_{n+1, i}
  = \frac{\partial}{\partial d_{n+1, i}} f(d_{n+1, i}, \dots)\cdot\text{sign}(x_{n+1} - x_{i})
\end{aligned}
$$
# Neighbors

$$
\mathcal{N}(n+1) = \{1 \leq i \leq n : \xi_{n+1, i} > \tau > 0\}
$$

# Potential field and force
Gains: $\alpha_{i}, \; \kappa_{i} \geq 0 \; \forall \; 1 \leq i \leq n$.
$$
\begin{aligned}
U_{n+1} &= \frac{1}{2}\sum_{i\in\mathcal{N}(n+1)}\kappa_{i}||x_{n+1} - \alpha_{i}(x_{i} + \xi_{n+1, i})||^{2}\\
F_{n+1} &= -\frac{\partial}{\partial x_{n+1}}\frac{1}{2}\sum_{i\in\mathcal{N}(n+1)}\kappa_{i}||x_{n+1} - \alpha_{i}(x_{i} + \xi_{n+1, i})||^{2}\\
&= -\sum_{i\in\mathcal{N}(n+1)}\kappa_{i}\big(x_{n+1} - \alpha_{i}(x_{i} + \xi_{n+1, i})\big)\frac{\partial}{\partial x_{n+1}}\big(x_{n+1} - \alpha_{i}(x_{i} + \xi_{n+1, i})\big)\\
&= -\sum_{i\in\mathcal{N}(n+1)}\kappa_{i}\big(x_{n+1} - \alpha_{i}(x_{i} + \xi_{n+1, i})\big)\big(1 - \alpha_{i}\frac{\partial}{\partial x_{n+1}}\xi_{n+1, i}\big)\\
&= -\sum_{i\in\mathcal{N}(n+1)}\kappa_{i}\big(x_{n+1} - \alpha_{i}(x_{i} + \xi_{n+1, i})\big)\big(1 - \alpha_{i}\frac{\partial}{\partial d_{n+1, i}} f(d_{n+1, i}, \dots)\cdot\text{sign}(x_{n+1} - x_{i})\big)\\
\end{aligned}
$$

Defining:
$$
\beta_{i} := \alpha_{i}\frac{\partial}{\partial d_{n+1, i}} f(d_{n+1, i}, \dots)
$$
Thus:

$$
\begin{aligned}
F_{n+1} &= -\sum_{i\in\mathcal{N}(n+1)}\kappa_{i}\big(x_{n+1} - \alpha_{i}(x_{i} + \xi_{n+1, i})\big)\big(1 - \beta_{i}\cdot\text{sign}(x_{n+1} - x_{i})\big)\\
\end{aligned}
$$

# Equilibrium point

$$
\begin{aligned}
  \mathcal{A}(n+1) &:= \{i\in\mathcal{N}(n+1): x_{n+1} - x_{i} > 0\} \implies \text{sign}(x_{n+1} - x_{i}) = 1\;\forall\;i\in\mathcal{A}\\
  \mathcal{B}(n+1) &:= \{i\in\mathcal{N}(n+1): x_{n+1} - x_{i} < 0\} \implies \text{sign}(x_{n+1} - x_{i}) = -1\;\forall\;i\in\mathcal{B}\\
  \mathcal{C}(n+1) &:= \{i\in\mathcal{N}(n+1): x_{n+1} - x_{i} = 0\} \implies \text{sign}(x_{n+1} - x_{i}) = 0\;\forall\;i\in\mathcal{C}\\
\end{aligned}
$$

$$
\begin{aligned}
F_{n+1} &= -\sum_{i\in\mathcal{N}(n+1)}\kappa_{i}\big(x_{n+1}^{*} - \alpha_{i}(x_{i} + \xi_{n+1, i})\big)\big(1 - \beta_{i}\cdot\text{sign}(x_{n+1}^{*} - x_{i})\big)\\
&= -\sum_{i\in\mathcal{A}(n+1)}\kappa_{i}\big(x_{n+1}^{*} - \alpha_{i}(x_{i} + \xi_{n+1, i})\big)(1 - \beta_{i})\\
&- \sum_{i\in\mathcal{B}(n+1)}\kappa_{i}\big(x_{n+1}^{*} - \alpha_{i}(x_{i} + \xi_{n+1, i})\big)(1 + \beta_{i})\\
&- \sum_{i\in\mathcal{C}(n+1)}\kappa_{i}\big(x_{n+1}^{*} - \alpha_{i}(x_{i} + \xi_{n+1, i})\big)(1)\\
&= -\sum_{i\in\mathcal{A}(n+1)}\kappa_{i}x_{n+1}^{*}(1 - \beta_{i}) + \sum_{i\in\mathcal{A}(n+1)}\kappa_{i}\alpha_{i}(x_{i} + \xi_{n+1, i})(1 - \beta_{i})\\
&-\sum_{i\in\mathcal{B}(n+1)}\kappa_{i}x_{n+1}^{*}(1 + \beta_{i}) + \sum_{i\in\mathcal{B}(n+1)}\kappa_{i}\alpha_{i}(x_{i} + \xi_{n+1, i})(1 + \beta_{i})\\
&-\sum_{i\in\mathcal{C}(n+1)}\kappa_{i}x_{n+1}^{*}(1) + \sum_{i\in\mathcal{C}(n+1)}\kappa_{i}\alpha_{i}(x_{i} + \xi_{n+1, i})(1)\\
&= -x_{n+1}^{*}\Bigg(\sum_{i\in\mathcal{A}(n+1)}\kappa_{i}(1 - \beta_{i}) + \sum_{i\in\mathcal{B}(n+1)}\kappa_{i}(1 + \beta_{i}) + \sum_{i\in\mathcal{C}(n+1)}\kappa_{i}\Bigg)\\
&+ \sum_{i\in\mathcal{A}(n+1)}\kappa_{i}\alpha_{i}(x_{i} + \xi_{n+1, i})(1 - \beta_{i})\\
&+ \sum_{i\in\mathcal{B}(n+1)}\kappa_{i}\alpha_{i}(x_{i} + \xi_{n+1, i})(1 + \beta_{i})\\
&+ \sum_{i\in\mathcal{C}(n+1)}\kappa_{i}\alpha_{i}(x_{i} + \xi_{n+1, i}) = 0\\
&\iff x_{n+1}^{*} = \frac{\sum_{i\in\mathcal{A}(n+1)}\kappa_{i}\alpha_{i}(x_{i} + \xi_{n+1, i})(1 - \beta_{i}) + \sum_{i\in\mathcal{B}(n+1)}\kappa_{i}\alpha_{i}(x_{i} + \xi_{n+1, i})(1 + \beta_{i}) + \sum_{i\in\mathcal{C}(n+1)}\kappa_{i}\alpha_{i}(x_{i} + \xi_{n+1, i})}
{\sum_{i\in\mathcal{A}(n+1)}\kappa_{i}(1 - \beta_{i}) + \sum_{i\in\mathcal{B}(n+1)}\kappa_{i}(1 + \beta_{i}) + \sum_{i\in\mathcal{C}(n+1)}\kappa_{i}}
\end{aligned}
$$


# Check

$$
\begin{aligned}
  x_{n+1} = x_{n+1}^{*} > \max_{i\in\mathcal{N}(n+1)}x_{i}^{*} = x_{m} & \iff \mathcal{A}(n+1) = \mathcal{N}(n+1),\;\mathcal{B}(n+1) = \mathcal{C}(n+1) = \emptyset,\; x_{n+1} = x_{n+1}^{*}\\
  &\iff \frac{\sum_{i\in\mathcal{N}(n+1)}\kappa_{i}\alpha_{i}(x_{i} + \xi_{n+1, i})(1 - \beta_{i})}{\sum_{i\in\mathcal{N}(n+1)}\kappa_{i}(1 - \beta_{i})} - x_{m} > 0
\end{aligned}
$$

Note: 
$$
\begin{aligned}
&\alpha_{i} \geq 0, \; \beta_{i} = \alpha_{i}\frac{\partial}{\partial d_{n+1, i}} f(d_{n+1, i}, \dots), \; \frac{\partial}{\partial d_{n+1, i}} f(d_{n+1, i}, \dots) \leq 0 \implies \beta_{i} \leq 0 \iff -\beta_{i} \geq 0\\
&\kappa_{i} \geq 0 , -\beta_{i} \geq 0 \implies \kappa_{i}(1-\beta_{i}) \geq 0 \implies \sum_{i\in\mathcal{N}(n+1)}\kappa_{i}(1-\beta_{i}) \geq 0 \quad (\text{strictly if } \exist \; i\in\mathcal{N}(n+1) \; \text{s.t. } \kappa_{i} > 0)
\end{aligned}
$$

Thus:

$$
\begin{aligned}
  x_{n+1} = x_{n+1}^{*} > \max_{i\in\mathcal{N}(n+1)}x_{i}^{*} = x_{m} & \iff \sum_{i\in\mathcal{N}(n+1)}\kappa_{i}\alpha_{i}(x_{i} + \xi_{n+1, i})(1 - \beta_{i}) - x_{m}\sum_{i\in\mathcal{N}(n+1)}\kappa_{i}(1 - \beta_{i}) > 0\\
  & \iff \sum_{i\in\mathcal{N}(n+1)}\kappa_{i}\alpha_{i}x_{i}(1 - \beta_{i}) + \sum_{i\in\mathcal{N}(n+1)}\kappa_{i}\alpha_{i}\xi_{n+1, i}(1 - \beta_{i}) - x_{m}\sum_{i\in\mathcal{N}(n+1)}\kappa_{i}(1 - \beta_{i}) > 0
\end{aligned}
$$

Defining
$$
-\beta_{i} \geq 0 \iff \gamma_{i} := 1-\beta_{i} \geq 1
$$

Thus:

$$
\begin{aligned}
  x_{n+1} = x_{n+1}^{*} > \max_{i\in\mathcal{N}(n+1)}x_{i}^{*} = x_{m} & \iff \sum_{i\in\mathcal{N}(n+1)}\kappa_{i}\alpha_{i}x_{i}\gamma_{i} + \sum_{i\in\mathcal{N}(n+1)}\kappa_{i}\alpha_{i}\xi_{n+1, i}\gamma_{i} - x_{m}\sum_{i\in\mathcal{N}(n+1)}\kappa_{i}\gamma_{i} > 0\\
  & \iff \kappa_{m}\alpha_{m}x_{m}\gamma_{m} + \sum_{i\in\mathcal{N}(n+1)\setminus\{m\}}\kappa_{i}\alpha_{i}x_{i}\gamma_{i} + \sum_{i\in\mathcal{N}(n+1)}\kappa_{i}\alpha_{i}\xi_{n+1, i}\gamma_{i} - x_{m}\sum_{i\in\mathcal{N}(n+1)}\kappa_{i}\gamma_{i} > 0\\
  & \iff x_{m}\Bigg(\kappa_{m}\alpha_{m}\gamma_{m} - \sum_{i\in\mathcal{N}(n+1)}\kappa_{i}\gamma_{i}\Bigg) + \sum_{i\in\mathcal{N}(n+1)\setminus\{m\}}\kappa_{i}\alpha_{i}x_{i}\gamma_{i} + \sum_{i\in\mathcal{N}(n+1)}\kappa_{i}\alpha_{i}\xi_{n+1, i}\gamma_{i} > 0\\
\end{aligned}
$$

We know:
$$
\begin{aligned}
&\kappa_{i} \geq 0, \; \alpha_{i} \geq 0, \; \gamma_{i} \geq 1, \; x_{i} \geq 0 \; \forall \; 1 \leq i \leq n\\
&\xi_{n+1, i} > \tau \; \forall \; i\in\mathcal{N}(n+1)
\end{aligned}
$$

Thus:

$$
\begin{aligned}
&\sum_{i\in\mathcal{N}(n+1)\setminus\{m\}}\kappa_{i}\alpha_{i}x_{i}\gamma_{i} \geq \sum_{i\in\mathcal{N}(n+1)\setminus\{m\}}\kappa_{i}\alpha_{i}x_{i}\cdot 1 \geq 0\\
&\sum_{i\in\mathcal{N}(n+1)}\kappa_{i}\alpha_{i}\xi_{n+1, i}\gamma_{i} > \sum_{i\in\mathcal{N}(n+1)}\kappa_{i}\alpha_{i}\cdot\tau\cdot 1 > 0 \iff \exist \; i\in\mathcal{N}(n+1) \text{ s.t. } \kappa_{i}, \alpha_{i} > 0
\end{aligned}
$$

In order for our statement to be true we must have:
$$
\begin{aligned}
  \kappa_{m}\alpha_{m}\gamma_{m} - \sum_{i\in\mathcal{N}(n+1)}\kappa_{i}\gamma_{i} \geq 0 & \iff \kappa_{m}\alpha_{m}\gamma_{m} - \kappa_{m}\gamma_{m} - \sum_{i\in\mathcal{N}(n+1)\setminus\{m\}}\kappa_{i}\gamma_{i} \geq 0\\
  & \iff \kappa_{m}\gamma_{m}(\alpha_{m} - 1) - \sum_{i\in\mathcal{N}(n+1)\setminus\{m\}}\kappa_{i}\gamma_{i} \geq 0\\
  & \iff \kappa_{m}\gamma_{m}(\alpha_{m} - 1) \geq \sum_{i\in\mathcal{N}(n+1)\setminus\{m\}}\kappa_{i}\gamma_{i}
\end{aligned}
$$

Assuming we know $\delta_{i} > 0$ such that:
$$
\begin{aligned}
  -\delta_{i} \leq \frac{\partial}{\partial d_{n+1, i}} f(d_{n+1, i}, \dots) \leq 0 & \iff -\alpha_{i}(-\delta_{i}) \geq -\alpha_{i}\frac{\partial}{\partial d_{n+1, i}} f(d_{n+1, i}, \dots) \geq -\alpha_{i} \cdot 0\\
  &\iff 1 + \alpha_{i}\delta_{i} \geq 1-\alpha_{i}\frac{\partial}{\partial d_{n+1, i}} f(d_{n+1, i}, \dots) \geq 1\\
  &\iff 1 + \alpha_{i}\delta_{i} \geq \gamma_{i} \geq 1\\
  &\iff \kappa_{i}(1 + \alpha_{i}\delta_{i}) \geq \kappa_{i}\gamma_{i} \geq \kappa_{i}\\
  &\iff -\kappa_{i}(1 + \alpha_{i}\delta_{i}) \leq -\kappa_{i}\gamma_{i} \leq -\kappa_{i}\\
\end{aligned}
$$

Choosing $\alpha_{m} > 1$ and using the statements above we get:

$$
\kappa_{m}\gamma_{m}(\alpha_{m} - 1) \geq \kappa_{m}(\alpha_{m} - 1),\quad \sum_{i\in\mathcal{N}(n+1)\setminus\{m\}}\kappa_{i}\gamma_{i} \leq \sum_{i\in\mathcal{N}(n+1)\setminus\{m\}}\kappa_{i}(1 + \alpha_{i}\delta_{i})
$$

$$
\kappa_{m}(\alpha_{m} - 1) \geq \sum_{i\in\mathcal{N}(n+1)\setminus\{m\}}\kappa_{i}(1 + \alpha_{i}\delta_{i}) \implies \kappa_{m}\gamma_{m}(\alpha_{m} - 1) \geq \sum_{i\in\mathcal{N}(n+1)\setminus\{m\}}\kappa_{i}\gamma_{i}
$$

Thus we have:

$$
\begin{aligned}
  x_{n+1} = x_{n+1}^{*} > \max_{i\in\mathcal{N}(n+1)}x_{i}^{*} = x_{m} & \iff x_{m}\Bigg(\kappa_{m}\alpha_{m}\gamma_{m} - \sum_{i\in\mathcal{N}(n+1)}\kappa_{i}\gamma_{i}\Bigg) + \sum_{i\in\mathcal{N}(n+1)\setminus\{m\}}\kappa_{i}\alpha_{i}x_{i}\gamma_{i} + \sum_{i\in\mathcal{N}(n+1)}\kappa_{i}\alpha_{i}\xi_{n+1, i}\gamma_{i} > 0\\
  & \iff \exist \; i\in\mathcal{N}(n+1) \text{ s.t. } \kappa_{i}, \alpha_{i} > 0,\quad \alpha_{m} > 1,\quad \kappa_{m}(\alpha_{m} - 1) \geq \sum_{i\in\mathcal{N}(n+1)\setminus\{m\}}\kappa_{i}(1 + \alpha_{i}\delta_{i})
\end{aligned}
$$


# Summary

Assuming we know $\delta_{i} \; \forall \; i\in\mathcal{N}(n+1)$ such that:

$$
-\delta_{i} \leq \frac{\partial}{\partial d_{n+1, i}} f(d_{n+1, i}, \dots) \leq 0 \; \forall \; i\in\mathcal{N}(n+1),
$$

meaning we know a lower bound on the decay rate of the RSSI.

Then, if we choose $\kappa_{i}$ and $\alpha_{i}$ such that:

$$
\exist \; i\in\mathcal{N}(n+1) \text{ s.t. } \kappa_{i}, \alpha_{i} > 0,\quad \alpha_{m} > 1,\quad \kappa_{m}(\alpha_{m} - 1) \geq \sum_{i\in\mathcal{N}(n+1)\setminus\{m\}}\kappa_{i}(1 + \alpha_{i}\delta_{i}),
$$
where $m = \argmax_{i\in\mathcal{N}(n+1)}x_{i}$, the drone $\nu_{n+1}$ is guaranteed to move beyond it's neighbors.

> ### Conditions for moving beyond neighbors
> 1. $\kappa_{i} \geq 0$
> 
> 2. $\alpha_{i} \geq 0$
> 
> 3. $\exist \; i\in\mathcal{N}(n+1) \text{ s.t. } \kappa_{i}, \alpha_{i} > 0$
>
> $m = \argmax_{i\in\mathcal{N}(n+1)}x_{i}$
>
> 4. $\alpha_{m} > 1$
>
> 5. $\kappa_{m}(\alpha_{m} - 1) \geq \sum_{i\in\mathcal{N}(n+1)\setminus\{m\}}\kappa_{i}(1 + \alpha_{i}\delta_{i})$

# Choosing gains
Assuming we have a already deployed set of drones $\nu_{1}, \nu_{2} \dots \nu_{n}$ such that $x_{1} < x_{2} < \dots < x_{n}$.

We know that for any neighbor set for drone $\nu_{n+1}$, $\mathcal{N}(n+1)$, it will be one the form:
$$
\mathcal{N}(n+1) = \{s, s+1, \dots s + |\mathcal{N}(n+1)| - 1\},
$$

where $1\leq s \leq n$. Furthermore we know that $m = \max \mathcal{N}(n+1) = s + |\mathcal{N}(n+1)| - 1$.

Choosing $\alpha_{i} = 2 \; \forall \; i \in\mathcal{N}(n+1)$ satisfies conditions 2 and 4. We must then choose $\kappa_{i}$s such that conditions 1, 3 and 5 are satisfied. From condition 5 we have:

$$
\begin{aligned}
\kappa_{m}(2 - 1) &\geq \sum_{i\in\mathcal{N}(n+1)\setminus\{m\}}\kappa_{i}(1 + 2\delta_{i}) = \sum_{i=s}^{s + |\mathcal{N}(n+1)| - 2}\kappa_{i}(1 + 2\delta_{i})\\
\kappa_{s + |\mathcal{N}(n+1)| - 1} &\geq \sum_{i=s}^{s + |\mathcal{N}(n+1)| - 2}\kappa_{i}(1 + 2\delta_{i})
\end{aligned}
$$

Assuming $\delta_{i} = \delta \; \forall \; 1 \leq i \leq n$ we get:

$$
\begin{aligned}
\kappa_{s + |\mathcal{N}(n+1)| - 1} &\geq (1 + 2\delta)\sum_{i=s}^{s + |\mathcal{N}(n+1)| - 2}\kappa_{i}
\end{aligned}
$$

Choosing $\tilde{\kappa}_{s + |\mathcal{N}(n+1)| - 1} = (1 + 2\delta)\kappa_{s + |\mathcal{N}(n+1)| - 1}$ we get:

$$
\begin{aligned}
\tilde{\kappa}_{s + |\mathcal{N}(n+1)| - 1} &\geq \sum_{i=s}^{s + |\mathcal{N}(n+1)| - 2}\kappa_{i}
\end{aligned}
$$

We want to find a function $g(\cdot): \mathbb{N}^{+} \rightarrow \mathbb{R}^{+}$ such that:

$$
g(t+1) \geq \sum_{i=s}^{t}g(i)
$$

A more restrictive function would be $g(\cdot)$ s.t.:

$$
g(t+1) \geq \sum_{i=0}^{t}g(i)
$$

> Suggestion: $g(i) = e^{i}$ (NUMERICALLY UNSTABLE FOR MANY NEIGHBORS)
> 
> $\kappa_{m} = \frac{1}{1 + 2\delta}e^{m}$, $\kappa_{i} = e^{i}, \; i \in \mathcal{N}(n+1)\setminus\{m\}$.

## TODO
Expand to 2D. What metric should be used to 'see if the new drone explores' more area?

## Straight to 2D

### Potential field and force
Gains: $\alpha_{i}, \; \kappa_{i} \geq 0 \; \forall \; 1 \leq i \leq n$. Added gain $\mathbf{v}_{i} = \begin{bmatrix}
  1 - \epsilon_{x} + \text{rand}(0, \epsilon_{x}) & 1 - \epsilon_{y} + \text{rand}(0, \epsilon_{y})
\end{bmatrix}^{T}$
$$
\begin{aligned}
U_{n+1} &= \frac{1}{2}\sum_{i\in\mathcal{N}(n+1)}\kappa_{i}||\mathbf{x}_{n+1} - \alpha_{i}(\mathbf{x}_{i} + \mathbf{v}_{i}\xi_{n+1, i})||^{2}\\
F_{n+1} &= -\frac{\partial}{\partial \mathbf{x}_{n+1}}\frac{1}{2}\sum_{i\in\mathcal{N}(n+1)}\kappa_{i}||\mathbf{x}_{n+1} - \alpha_{i}(\mathbf{x}_{i} + \mathbf{v}_{i}\xi_{n+1, i})||^{2}\\
&= -\sum_{i\in\mathcal{N}(n+1)}\frac{\partial}{\partial \mathbf{x}_{n+1}}\big(\mathbf{x}_{n+1} - \alpha_{i}(\mathbf{x}_{i} + \mathbf{v}_{i}\xi_{n+1, i})\big)\kappa_{i}\big(\mathbf{x}_{n+1} - \alpha_{i}(\mathbf{x}_{i} + \mathbf{v}_{i}\xi_{n+1, i})\big)\\
&= -\sum_{i\in\mathcal{N}(n+1)}\big(\mathbf{I} - \alpha_{i}\frac{\partial}{\partial \mathbf{x}_{n+1}}\mathbf{v}_{i}\xi_{n+1, i}\big)\kappa_{i}\big(\mathbf{x}_{n+1} - \alpha_{i}(\mathbf{x}_{i} + \mathbf{v}_{i}\xi_{n+1, i})\big)\\
&= -\sum_{i\in\mathcal{N}(n+1)}\kappa_{i}\big(\mathbf{I} - \alpha_{i}\frac{\partial}{\partial d_{n+1, i}}f(d_{n+1, i}, \dots)\frac{\mathbf{x}_{n+1} - \mathbf{x}_{i}}{||\mathbf{x}_{n+1} - \mathbf{x}_{i}||}\mathbf{v}_{i}^{T}\big)\big(\mathbf{x}_{n+1} - \alpha_{i}(\mathbf{x}_{i} + \mathbf{v}_{i}\xi_{n+1, i})\big)\\
\end{aligned}
$$

### Checking for larger dispersion
$$
\mathbf{Q} = \frac{1}{n-1}\sum_{i=1}^{n}(\mathbf{s}_{i}-\mathbf{c})(\mathbf{s}_{i}-\mathbf{c})^{T},\quad \mathbf{c} = \frac{1}{n}\sum_{i=1}^{n}\mathbf{s}_{i}
$$

> "The generalized variance is defined as the determinant of the covariance matrix, $\det(\Sigma)$. It can be shown to be related to the multidimensional scatter of points around their mean."

**TODO**: Check if $\det{(\mathbf{Q})}$ is larger after $\mathbf{x}_{n+1} = \mathbf{x}_{n+1}^{*}$ is included than when only using neighbors.

For a set $\mathcal{S}$ of drones $\nu_{i},\;i\in\mathcal{S}$ positioned at $\mathbf{x}_{i}\in\mathbb{R}^{2}$, the generalized variance is defined as:
$$
\begin{aligned}
\det(\mathbf{Q}_{\mathcal{S}}) &= \det\Bigg(\frac{1}{|\mathcal{S}|-1}\sum_{i\in\mathcal{S}}(\mathbf{x}_{i}-\mathbf{c}_{\mathcal{S}})(\mathbf{x}_{i}-\mathbf{c}_{\mathcal{S}})^{T}\Bigg) = \Bigg(\frac{1}{|\mathcal{S}|-1}\Bigg)^{2}\det\Bigg(\sum_{i\in\mathcal{S}}\begin{bmatrix}
  x_{i} - c_{\mathcal{S}, x}\\
  y_{i} - c_{\mathcal{S}, y}
\end{bmatrix}\begin{bmatrix}
  x_{i} - c_{\mathcal{S}, x}&
  y_{i} - c_{\mathcal{S}, y}
\end{bmatrix}\Bigg)\\
&= \Bigg(\frac{1}{|\mathcal{S}|-1}\Bigg)^{2}\det\Bigg(\sum_{i\in\mathcal{S}}\begin{bmatrix}
  (x_{i} - c_{\mathcal{S}, x})^{2} & (x_{i} - c_{\mathcal{S}, x})(y_{i} - c_{\mathcal{S}, y})\\
  \dots & (y_{i} - c_{\mathcal{S}, y})^{2}
\end{bmatrix}\Bigg)\\
&= \Bigg(\frac{1}{|\mathcal{S}|-1}\Bigg)^{2}\det\Bigg(\begin{bmatrix}
  \sum_{i\in\mathcal{S}}(x_{i} - c_{\mathcal{S}, x})^{2} & \sum_{i\in\mathcal{S}}(x_{i} - c_{\mathcal{S}, x})(y_{i} - c_{\mathcal{S}, y})\\
  \dots & \sum_{i\in\mathcal{S}}(y_{i} - c_{\mathcal{S}, y})^{2}
\end{bmatrix}\Bigg)\\
&= \Bigg(\frac{1}{|\mathcal{S}|-1}\Bigg)^{2}\Bigg(
  \Big(\sum_{i\in\mathcal{S}}(x_{i} - c_{\mathcal{S}, x})^{2}\Big)\Big(\sum_{i\in\mathcal{S}}(y_{i} - c_{\mathcal{S}, y})^{2}\Big) - \Big(\sum_{i\in\mathcal{S}}(x_{i} - c_{\mathcal{S}, x})(y_{i} - c_{\mathcal{S}, y})\Big)^{2}
\Bigg)\\
\end{aligned}
$$

Defining the column vectors:
$$
\begin{aligned}
\mathbf{x}_{\mathcal{S}} &= \begin{bmatrix}
  x_{i}
\end{bmatrix}\in\mathbb{R}^{|\mathcal{S}|\times 1}\\
\mathbf{y}_{\mathcal{S}} &= \begin{bmatrix}
  y_{i}
\end{bmatrix}\in\mathbb{R}^{|\mathcal{S}|\times 1}\\
\mathbf{d}_{\mathcal{S}, x} &= \begin{bmatrix}
  x_{i} - c_{\mathcal{S}, x}
\end{bmatrix} = \mathbf{x}_{\mathcal{S}} - \mathbf{1}
c_{\mathcal{S}, x}\in\mathbb{R}^{|\mathcal{S}|\times 1}\\
\mathbf{d}_{\mathcal{S}, y} &= \begin{bmatrix}
  y_{i} - c_{\mathcal{S}, y}
\end{bmatrix} = \mathbf{y}_{\mathcal{S}} - \mathbf{1}
c_{\mathcal{S}, y}\in\mathbb{R}^{|\mathcal{S}|\times 1}\\
\end{aligned}
$$

so that:

$$
\begin{aligned}
  \mathbf{d}_{\mathcal{S}, x}^{T}\mathbf{d}_{\mathcal{S}, x} = \begin{bmatrix}
    x_{\mathcal{S}_{1}} - c_{\mathcal{S}, x}&
    x_{\mathcal{S}_{2}} - c_{\mathcal{S}, x}&
    \dots&
    x_{\mathcal{S}_{|\mathcal{S}|}} - c_{\mathcal{S}, x}
  \end{bmatrix}\begin{bmatrix}
    x_{\mathcal{S}_{1}} - c_{\mathcal{S}, x}\\
    x_{\mathcal{S}_{2}} - c_{\mathcal{S}, x}\\
    \vdots\\
    x_{\mathcal{S}_{|\mathcal{S}|}} - c_{\mathcal{S}, x}
  \end{bmatrix} &= \sum_{i\in\mathcal{S}}(x_{i} - c_{\mathcal{S}, x})^{2}\\

  \mathbf{d}_{\mathcal{S}, y}^{T}\mathbf{d}_{\mathcal{S}, y} = \begin{bmatrix}
    y_{\mathcal{S}_{1}} - c_{\mathcal{S}, y}&
    y_{\mathcal{S}_{2}} - c_{\mathcal{S}, y}&
    \dots&
    y_{\mathcal{S}_{|\mathcal{S}|}} - c_{\mathcal{S}, y}
  \end{bmatrix}\begin{bmatrix}
    y_{\mathcal{S}_{1}} - c_{\mathcal{S}, y}\\
    y_{\mathcal{S}_{2}} - c_{\mathcal{S}, y}\\
    \vdots\\
    y_{\mathcal{S}_{|\mathcal{S}|}} - c_{\mathcal{S}, y}
  \end{bmatrix} &= \sum_{i\in\mathcal{S}}(y_{i} - c_{\mathcal{S}, y})^{2}\\

  \mathbf{d}_{\mathcal{S}, x}^{T}\mathbf{d}_{\mathcal{S}, y} = \begin{bmatrix}
    x_{\mathcal{S}_{1}} - c_{\mathcal{S}, x}&
    x_{\mathcal{S}_{2}} - c_{\mathcal{S}, x}&
    \dots&
    x_{\mathcal{S}_{|\mathcal{S}|}} - c_{\mathcal{S}, x}
  \end{bmatrix}\begin{bmatrix}
    y_{\mathcal{S}_{1}} - c_{\mathcal{S}, y}\\
    y_{\mathcal{S}_{2}} - c_{\mathcal{S}, y}\\
    \vdots\\
    y_{\mathcal{S}_{|\mathcal{S}|}} - c_{\mathcal{S}, y}
  \end{bmatrix} &= \sum_{i\in\mathcal{S}}(x_{i} - c_{\mathcal{S}, x})(y_{i} - c_{\mathcal{S}, y})\\
\end{aligned}
$$

we arrive at:

$$
\det(\mathbf{Q}_{\mathcal{S}}) = \Bigg(\frac{1}{|\mathcal{S}|-1}\Bigg)^{2}\Big(
  \mathbf{d}_{\mathcal{S}, x}^{T}\mathbf{d}_{\mathcal{S}, x}\mathbf{d}_{\mathcal{S}, y}^{T}\mathbf{d}_{\mathcal{S}, y} - \big(\mathbf{d}_{\mathcal{S}, x}^{T}\mathbf{d}_{\mathcal{S}, y}\big)^{2}
\Big)
$$

#### Check for increase in generalized variance
Assuming $|\mathcal{N}(n+1)| \geq 2$.
$\mathcal{S}(n+1) := \mathcal{N}(n+1)\cup\{n+1\}$
$$
\begin{aligned}
  \det(\mathbf{Q}_{\mathcal{S}(n+1)}) > \det(\mathbf{Q}_{\mathcal{N}(n+1)}) &\iff \Bigg(\frac{1}{|\mathcal{S}(n+1)|-1}\Bigg)^{2}\Big(
  \mathbf{d}_{\mathcal{S}(n+1), x}^{T}\mathbf{d}_{\mathcal{S}(n+1), x}\mathbf{d}_{\mathcal{S}(n+1), y}^{T}\mathbf{d}_{\mathcal{S}(n+1), y} - \big(\mathbf{d}_{\mathcal{S}(n+1), x}^{T}\mathbf{d}_{\mathcal{S}(n+1), y}\big)^{2} > \Bigg(\frac{1}{|\mathcal{N}(n+1)|-1}\Bigg)^{2}\Big(
  \mathbf{d}_{\mathcal{N}(n+1), x}^{T}\mathbf{d}_{\mathcal{N}(n+1), x}\mathbf{d}_{\mathcal{N}(n+1), y}^{T}\mathbf{d}_{\mathcal{N}(n+1), y} - \big(\mathbf{d}_{\mathcal{N}(n+1), x}^{T}\mathbf{d}_{\mathcal{N}(n+1), y}\big)^{2}
\Big)\\
& \iff \Bigg(\frac{1}{|\mathcal{N}(n+1)| + 1 - 1}\Bigg)^{2}\Big(
  \mathbf{d}_{\mathcal{S}(n+1), x}^{T}\mathbf{d}_{\mathcal{S}(n+1), x}\mathbf{d}_{\mathcal{S}(n+1), y}^{T}\mathbf{d}_{\mathcal{S}(n+1), y} - \big(\mathbf{d}_{\mathcal{S}(n+1), x}^{T}\mathbf{d}_{\mathcal{S}(n+1), y}\big)^{2} > \Bigg(\frac{1}{|\mathcal{N}(n+1)|-1}\Bigg)^{2}\Big(
  \mathbf{d}_{\mathcal{N}(n+1), x}^{T}\mathbf{d}_{\mathcal{N}(n+1), x}\mathbf{d}_{\mathcal{N}(n+1), y}^{T}\mathbf{d}_{\mathcal{N}(n+1), y} - \big(\mathbf{d}_{\mathcal{N}(n+1), x}^{T}\mathbf{d}_{\mathcal{N}(n+1), y}\big)^{2}
\Big)\\
& \iff
  \mathbf{d}_{\mathcal{S}(n+1), x}^{T}\mathbf{d}_{\mathcal{S}(n+1), x}\mathbf{d}_{\mathcal{S}(n+1), y}^{T}\mathbf{d}_{\mathcal{S}(n+1), y} - \big(\mathbf{d}_{\mathcal{S}(n+1), x}^{T}\mathbf{d}_{\mathcal{S}(n+1), y}\big)^{2} - \Bigg(\frac{|\mathcal{N}(n+1)|}{|\mathcal{N}(n+1)|-1}\Bigg)^{2}\Big(
  \mathbf{d}_{\mathcal{N}(n+1), x}^{T}\mathbf{d}_{\mathcal{N}(n+1), x}\mathbf{d}_{\mathcal{N}(n+1), y}^{T}\mathbf{d}_{\mathcal{N}(n+1), y} - \big(\mathbf{d}_{\mathcal{N}(n+1), x}^{T}\mathbf{d}_{\mathcal{N}(n+1), y}\big)^{2}\Big) > 0
\end{aligned}
$$

---

$$
\begin{aligned}
c_{\mathcal{S}(n+1), x} &= \frac{1}{|\mathcal{S}(n+1)|}\sum_{i\in\mathcal{S}(n+1)}x_{i} = \frac{1}{|\mathcal{N}(n+1)|+1}\Big(x_{n+1} + \sum_{i\in\mathcal{N}(n+1)}x_{i}\Big) = \frac{1}{|\mathcal{N}(n+1)|+1}\Big(x_{n+1} + |\mathcal{N}(n+1)|\frac{1}{|\mathcal{N}(n+1)|}\sum_{i\in\mathcal{N}(n+1)}x_{i}\Big)\\
&= \frac{1}{|\mathcal{N}(n+1)|+1}\Big(x_{n+1} + |\mathcal{N}(n+1)|c_{\mathcal{N}(n+1), x}\Big)\\


\mathbf{x}_{\mathcal{S}(n+1), x} &= \begin{bmatrix}
  \mathbf{x}_{\mathcal{N}(n+1), x}\\
  x_{n+1}
\end{bmatrix} = \begin{bmatrix}
  \mathbf{d}_{\mathcal{N}(n+1), x} + \mathbf{1}c_{\mathcal{N}(n+1), x}\\
  x_{n+1}
\end{bmatrix}\\


\implies \mathbf{d}_{\mathcal{S}(n+1), x} &= \mathbf{x}_{\mathcal{S}(n+1)} - \mathbf{1}c_{\mathcal{S}(n+1), x} = \begin{bmatrix}
  \mathbf{d}_{\mathcal{N}(n+1), x} + \mathbf{1}c_{\mathcal{N}(n+1), x}\\
  x_{n+1}
\end{bmatrix} - \mathbf{1}\frac{1}{|\mathcal{N}(n+1)|+1}\Big(x_{n+1} + |\mathcal{N}(n+1)|c_{\mathcal{N}(n+1), x}\Big)\\
&= \begin{bmatrix}
  \mathbf{d}_{\mathcal{N}(n+1), x} + \mathbf{1}c_{\mathcal{N}(n+1), x} - \mathbf{1}\frac{1}{|\mathcal{N}(n+1)|+1}x_{n+1} - \mathbf{1}\frac{|\mathcal{N}(n+1)|}{|\mathcal{N}(n+1)|+1}c_{\mathcal{N}(n+1), x}\\
  x_{n+1} - \frac{1}{|\mathcal{N}(n+1)|+1}\Big(x_{n+1} + |\mathcal{N}(n+1)|c_{\mathcal{N}(n+1), x}\Big)
\end{bmatrix}\\
&= \begin{bmatrix}
  \mathbf{d}_{\mathcal{N}(n+1), x} + \mathbf{1}\frac{1}{|\mathcal{N}(n+1)|+1}(c_{\mathcal{N}(n+1), x} - x_{n+1})\\
  \frac{|\mathcal{N}(n+1)|}{|\mathcal{N}(n+1)|+1}(x_{n+1} - c_{\mathcal{N}(n+1), x})
\end{bmatrix}\\
&= \begin{bmatrix}
  \mathbf{d}_{\mathcal{N}(n+1), x}\\
  0
\end{bmatrix}+\frac{1}{|\mathcal{N}(n+1)|+1}\begin{bmatrix}
  -\mathbf{1}\\
  |\mathcal{N}(n+1)|
\end{bmatrix}(x_{n+1}-c_{\mathcal{N}(n+1), x})\\
\implies \mathbf{d}_{\mathcal{S}(n+1), y} &= \begin{bmatrix}
  \mathbf{d}_{\mathcal{N}(n+1), y}\\
  0
\end{bmatrix}+\frac{1}{|\mathcal{N}(n+1)|+1}\begin{bmatrix}
  -\mathbf{1}\\
  |\mathcal{N}(n+1)|
\end{bmatrix}(y_{n+1}-c_{\mathcal{N}(n+1), y})
\end{aligned}
$$

Defining:

$$
\begin{aligned}
  \bar{\mathbf{d}}_{\mathcal{N}(n+1), x} &= \begin{bmatrix}
    \mathbf{d}_{\mathcal{N}(n+1), x}\\
    0
  \end{bmatrix}\\
  \bar{\mathbf{d}}_{\mathcal{N}(n+1), y} &= \begin{bmatrix}
    \mathbf{d}_{\mathcal{N}(n+1), y}\\
    0
  \end{bmatrix}\\
  \boldsymbol{\delta}_{n+1, x} &:= \frac{1}{|\mathcal{N}(n+1)|+1}\begin{bmatrix}
  -\mathbf{1}\\
  |\mathcal{N}(n+1)|
\end{bmatrix}(x_{n+1}-c_{\mathcal{N}(n+1), x})\\
\boldsymbol{\delta}_{n+1, y} &:= \frac{1}{|\mathcal{N}(n+1)|+1}\begin{bmatrix}
  -\mathbf{1}\\
  |\mathcal{N}(n+1)|
\end{bmatrix}(y_{n+1}-c_{\mathcal{N}(n+1), y})\\
\end{aligned}
$$

we get:

$$
\begin{aligned}
  \mathbf{d}_{\mathcal{S}(n+1), x} &=\bar{\mathbf{d}}_{\mathcal{N}(n+1), x} + \boldsymbol{\delta}_{n+1, x}\\
  \mathbf{d}_{\mathcal{S}(n+1), y} &=\bar{\mathbf{d}}_{\mathcal{N}(n+1), y} + \boldsymbol{\delta}_{n+1, y}\\
\end{aligned}
$$

$$
\begin{aligned}
\mathbf{d}_{\mathcal{S}(n+1), x}^{T}\mathbf{d}_{\mathcal{S}(n+1), x} &= \big(\bar{\mathbf{d}}_{\mathcal{N}(n+1), x} + \boldsymbol{\delta}_{n+1, x}\big)^{T}\big(\bar{\mathbf{d}}_{\mathcal{N}(n+1), x} + \boldsymbol{\delta}_{n+1, x}\big) = \bar{\mathbf{d}}_{\mathcal{N}(n+1), x}^{T}\bar{\mathbf{d}}_{\mathcal{N}(n+1), x} + \bar{\mathbf{d}}_{\mathcal{N}(n+1), x}^{T}\boldsymbol{\delta}_{n+1, x} + \boldsymbol{\delta}_{n+1, x}^{T}\bar{\mathbf{d}}_{\mathcal{N}(n+1), x} + \boldsymbol{\delta}_{n+1, x}^{T}\boldsymbol{\delta}_{n+1, x}\\
&= \mathbf{d}_{\mathcal{N}(n+1), x}^{T}\mathbf{d}_{\mathcal{N}(n+1), x} + \boldsymbol{\delta}_{n+1, x}^{T}\boldsymbol{\delta}_{n+1, x} + 2\bar{\mathbf{d}}_{\mathcal{N}(n+1), x}^{T}\boldsymbol{\delta}_{n+1, x}\\

\mathbf{d}_{\mathcal{S}(n+1), y}^{T}\mathbf{d}_{\mathcal{S}(n+1), y} &= \mathbf{d}_{\mathcal{N}(n+1), y}^{T}\mathbf{d}_{\mathcal{N}(n+1), y} + \boldsymbol{\delta}_{n+1, y}^{T}\boldsymbol{\delta}_{n+1, y} + 2\bar{\mathbf{d}}_{\mathcal{N}(n+1), y}^{T}\boldsymbol{\delta}_{n+1, y}
\end{aligned}
$$

$$
\begin{aligned}
  \mathbf{d}_{\mathcal{S}(n+1), x}^{T}\mathbf{d}_{\mathcal{S}(n+1), x}\mathbf{d}_{\mathcal{S}(n+1), y}^{T}\mathbf{d}_{\mathcal{S}(n+1), y} &= 
  \big(
    \mathbf{d}_{\mathcal{N}(n+1), x}^{T}\mathbf{d}_{\mathcal{N}(n+1), x} + \boldsymbol{\delta}_{n+1, x}^{T}\boldsymbol{\delta}_{n+1, x} + 2\bar{\mathbf{d}}_{\mathcal{N}(n+1), x}^{T}\boldsymbol{\delta}_{n+1, x}
  \big)
  \big(
    \mathbf{d}_{\mathcal{N}(n+1), y}^{T}\mathbf{d}_{\mathcal{N}(n+1), y} + \boldsymbol{\delta}_{n+1, y}^{T}\boldsymbol{\delta}_{n+1, y} + 2\bar{\mathbf{d}}_{\mathcal{N}(n+1), y}^{T}\boldsymbol{\delta}_{n+1, y}
  \big)\\
  &= \mathbf{d}_{\mathcal{N}(n+1), x}^{T}\mathbf{d}_{\mathcal{N}(n+1), x}\mathbf{d}_{\mathcal{N}(n+1), y}^{T}\mathbf{d}_{\mathcal{N}(n+1), y} + \mathbf{d}_{\mathcal{N}(n+1), x}^{T}\mathbf{d}_{\mathcal{N}(n+1), x}(\boldsymbol{\delta}_{n+1, y}^{T}\boldsymbol{\delta}_{n+1, y} + 2\bar{\mathbf{d}}_{\mathcal{N}(n+1), y}^{T}\boldsymbol{\delta}_{n+1, y})\\
  &+ (\boldsymbol{\delta}_{n+1, x}^{T}\boldsymbol{\delta}_{n+1, x} + 2\bar{\mathbf{d}}_{\mathcal{N}(n+1), x}^{T}\boldsymbol{\delta}_{n+1, x})(\mathbf{d}_{\mathcal{N}(n+1), y}^{T}\mathbf{d}_{\mathcal{N}(n+1), y} + \boldsymbol{\delta}_{n+1, y}^{T}\boldsymbol{\delta}_{n+1, y} + 2\bar{\mathbf{d}}_{\mathcal{N}(n+1), y}^{T}\boldsymbol{\delta}_{n+1, y})
\end{aligned}
$$

$$
\begin{aligned}
  \big(\mathbf{d}_{\mathcal{S}(n+1), x}^{T}\mathbf{d}_{\mathcal{S}(n+1), y}\big)^{2} &= \big((\bar{\mathbf{d}}_{\mathcal{N}(n+1), x} + \boldsymbol{\delta}_{n+1, x})^{T}(\bar{\mathbf{d}}_{\mathcal{N}(n+1), y} + \boldsymbol{\delta}_{n+1, y})\big)^{2} = \big(
    \mathbf{d}_{\mathcal{N}(n+1), x}^{T}\mathbf{d}_{\mathcal{N}(n+1), y} + 
    \bar{\mathbf{d}}_{\mathcal{N}(n+1), x}^{T}\boldsymbol{\delta}_{n+1, y} + \boldsymbol{\delta}_{n+1, x}^{T}\bar{\mathbf{d}}_{\mathcal{N}(n+1), y} + \boldsymbol{\delta}_{n+1, x}^{T}\boldsymbol{\delta}_{n+1, y}
  \big)^{2}\\
  &= (\mathbf{d}_{\mathcal{N}(n+1), x}^{T}\mathbf{d}_{\mathcal{N}(n+1), y})^{2} + 2\mathbf{d}_{\mathcal{N}(n+1), x}^{T}\mathbf{d}_{\mathcal{N}(n+1), y}(\bar{\mathbf{d}}_{\mathcal{N}(n+1), x}^{T}\boldsymbol{\delta}_{n+1, y} + \boldsymbol{\delta}_{n+1, x}^{T}\bar{\mathbf{d}}_{\mathcal{N}(n+1), y} + \boldsymbol{\delta}_{n+1, x}^{T}\boldsymbol{\delta}_{n+1, y})\\
  &+ (\bar{\mathbf{d}}_{\mathcal{N}(n+1), x}^{T}\boldsymbol{\delta}_{n+1, y} + \boldsymbol{\delta}_{n+1, x}^{T}\bar{\mathbf{d}}_{\mathcal{N}(n+1), y} + \boldsymbol{\delta}_{n+1, x}^{T}\boldsymbol{\delta}_{n+1, y})^{2}
\end{aligned}
$$

---

$$
\begin{aligned}
  &\mathbf{d}_{\mathcal{S}(n+1), x}^{T}\mathbf{d}_{\mathcal{S}(n+1), x}\mathbf{d}_{\mathcal{S}(n+1), y}^{T}\mathbf{d}_{\mathcal{S}(n+1), y} - \big(\mathbf{d}_{\mathcal{S}(n+1), x}^{T}\mathbf{d}_{\mathcal{S}(n+1), y}\big)^{2} - \Bigg(\frac{|\mathcal{N}(n+1)|}{|\mathcal{N}(n+1)|-1}\Bigg)^{2}\Big(
  \mathbf{d}_{\mathcal{N}(n+1), x}^{T}\mathbf{d}_{\mathcal{N}(n+1), x}\mathbf{d}_{\mathcal{N}(n+1), y}^{T}\mathbf{d}_{\mathcal{N}(n+1), y} - \big(\mathbf{d}_{\mathcal{N}(n+1), x}^{T}\mathbf{d}_{\mathcal{N}(n+1), y}\big)^{2}\Big) = \\


  &\mathbf{d}_{\mathcal{N}(n+1), x}^{T}\mathbf{d}_{\mathcal{N}(n+1), x}\mathbf{d}_{\mathcal{N}(n+1), y}^{T}\mathbf{d}_{\mathcal{N}(n+1), y} + \mathbf{d}_{\mathcal{N}(n+1), x}^{T}\mathbf{d}_{\mathcal{N}(n+1), x}(\boldsymbol{\delta}_{n+1, y}^{T}\boldsymbol{\delta}_{n+1, y} + 2\bar{\mathbf{d}}_{\mathcal{N}(n+1), y}^{T}\boldsymbol{\delta}_{n+1, y}) + \\
  & (\boldsymbol{\delta}_{n+1, x}^{T}\boldsymbol{\delta}_{n+1, x} + 2\bar{\mathbf{d}}_{\mathcal{N}(n+1), x}^{T}\boldsymbol{\delta}_{n+1, x})(\mathbf{d}_{\mathcal{N}(n+1), y}^{T}\mathbf{d}_{\mathcal{N}(n+1), y} + \boldsymbol{\delta}_{n+1, y}^{T}\boldsymbol{\delta}_{n+1, y} + 2\bar{\mathbf{d}}_{\mathcal{N}(n+1), y}^{T}\boldsymbol{\delta}_{n+1, y}) + \\
  &(\mathbf{d}_{\mathcal{N}(n+1), x}^{T}\mathbf{d}_{\mathcal{N}(n+1), y})^{2} + 2\mathbf{d}_{\mathcal{N}(n+1), x}^{T}\mathbf{d}_{\mathcal{N}(n+1), y}(\bar{\mathbf{d}}_{\mathcal{N}(n+1), x}^{T}\boldsymbol{\delta}_{n+1, y} + \boldsymbol{\delta}_{n+1, x}^{T}\bar{\mathbf{d}}_{\mathcal{N}(n+1), y} + \boldsymbol{\delta}_{n+1, x}^{T}\boldsymbol{\delta}_{n+1, y}) + \\
  & (\bar{\mathbf{d}}_{\mathcal{N}(n+1), x}^{T}\boldsymbol{\delta}_{n+1, y} + \boldsymbol{\delta}_{n+1, x}^{T}\bar{\mathbf{d}}_{\mathcal{N}(n+1), y} + \boldsymbol{\delta}_{n+1, x}^{T}\boldsymbol{\delta}_{n+1, y})^{2} - \\
  &\Bigg(\frac{|\mathcal{N}(n+1)|}{|\mathcal{N}(n+1)|-1}\Bigg)^{2}\Big(
  \mathbf{d}_{\mathcal{N}(n+1), x}^{T}\mathbf{d}_{\mathcal{N}(n+1), x}\mathbf{d}_{\mathcal{N}(n+1), y}^{T}\mathbf{d}_{\mathcal{N}(n+1), y} - (\mathbf{d}_{\mathcal{N}(n+1), x}^{T}\mathbf{d}_{\mathcal{N}(n+1), y})^{2}\Big) = \\

  &\mathbf{d}_{\mathcal{N}(n+1), x}^{T}\mathbf{d}_{\mathcal{N}(n+1), x}\mathbf{d}_{\mathcal{N}(n+1), y}^{T}\mathbf{d}_{\mathcal{N}(n+1), y}\big(1 - g(|\mathcal{N}(n+1|)\big) + \\
  &(\mathbf{d}_{\mathcal{N}(n+1), x}^{T}\mathbf{d}_{\mathcal{N}(n+1), y})^{2}\big(1 + g(|\mathcal{N}(n+1|)\big) + \\
  &\mathbf{d}_{\mathcal{N}(n+1), x}^{T}\mathbf{d}_{\mathcal{N}(n+1), x}(\boldsymbol{\delta}_{n+1, y}^{T}\boldsymbol{\delta}_{n+1, y} + 2\bar{\mathbf{d}}_{\mathcal{N}(n+1), y}^{T}\boldsymbol{\delta}_{n+1, y}) + \\
  & (\boldsymbol{\delta}_{n+1, x}^{T}\boldsymbol{\delta}_{n+1, x} + 2\bar{\mathbf{d}}_{\mathcal{N}(n+1), x}^{T}\boldsymbol{\delta}_{n+1, x})(\mathbf{d}_{\mathcal{N}(n+1), y}^{T}\mathbf{d}_{\mathcal{N}(n+1), y} + \boldsymbol{\delta}_{n+1, y}^{T}\boldsymbol{\delta}_{n+1, y} + 2\bar{\mathbf{d}}_{\mathcal{N}(n+1), y}^{T}\boldsymbol{\delta}_{n+1, y}) + \\
  &2\mathbf{d}_{\mathcal{N}(n+1), x}^{T}\mathbf{d}_{\mathcal{N}(n+1), y}(\bar{\mathbf{d}}_{\mathcal{N}(n+1), x}^{T}\boldsymbol{\delta}_{n+1, y} + \boldsymbol{\delta}_{n+1, x}^{T}\bar{\mathbf{d}}_{\mathcal{N}(n+1), y} + \boldsymbol{\delta}_{n+1, x}^{T}\boldsymbol{\delta}_{n+1, y}) + \\
  & (\bar{\mathbf{d}}_{\mathcal{N}(n+1), x}^{T}\boldsymbol{\delta}_{n+1, y} + \boldsymbol{\delta}_{n+1, x}^{T}\bar{\mathbf{d}}_{\mathcal{N}(n+1), y} + \boldsymbol{\delta}_{n+1, x}^{T}\boldsymbol{\delta}_{n+1, y})^{2} = \\

\end{aligned}
$$


**TODO**
Read papers about entropy.

