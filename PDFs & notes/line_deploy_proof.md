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
> $\kappa_{m} = \frac{1}{1 + 2\delta}e^{m}$, $\kappa_{i}$

## TODO
Expand to 2D. What metric should be used to 'see if the new drone explores' more area?
