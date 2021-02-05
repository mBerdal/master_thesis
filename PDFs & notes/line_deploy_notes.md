## 1D Line deploy
### Potential field affecting drone $\nu_{n+1}$
$$
U_{n+1} = \frac{1}{2}\sum_{i=1}^{n}\kappa_{i}||x_{n+1}-x_{i}-\xi_{n+1,i}||^{2}
$$
### Force field affecting drone $\nu_{n+1}$
$$
\begin{aligned}
F_{n+1} &= -\frac{\partial}{\partial x_{n+1}}U_{n+1} = -\frac{1}{2}\sum_{i=1}^{n}\kappa_{i}\frac{\partial}{\partial x_{n+1}}||x_{n+1}-x_{i}-\xi_{n+1,i}||^{2}\\
&=-\frac{1}{2}\sum_{i=1}^{n}\kappa_{i}\frac{\partial}{\partial x_{n+1}}(x_{n+1}-x_{i}-\xi_{n+1,i})^{2}\\
&=-\frac{1}{2}\sum_{i=1}^{n}\kappa_{i}2(x_{n+1}-x_{i}-\xi_{n+1,i})\frac{\partial}{\partial x_{n+1}}(x_{n+1}-x_{i}-\xi_{n+1,i})\\
&=-\sum_{i=1}^{n}\kappa_{i}(x_{n+1}-x_{i}-\xi_{n+1,i})\\
&=\sum_{i=1}^{n}\kappa_{i}(x_{i}-x_{n+1}+\xi_{n+1,i})\\
\end{aligned}
$$

### Equilibrium point for drone $\nu_{n+1}$
$$
\begin{aligned}
  x_{n+1} = x_{n+1}^{*}&\iff F_{n+1} = 0\\
  &\iff  =\sum_{i=1}^{n}\kappa_{i}(x_{i}-x_{n+1}^{*}+\xi_{n+1,i})=0\\
  &\iff -x_{n+1}^{*}\sum_{i=1}^{n}\kappa_{i} + \sum_{i=1}^{n}\kappa_{i}(x_{i}+\xi_{n+1, i}) = 0\\
  &\iff x_{n+1}^{*} = \frac{\sum_{i=1}^{n}\kappa_{i}(x_{i}+\xi_{n+1, i})}{\sum_{i=1}^{n}\kappa_{i}}\\
\end{aligned}
$$
It is assumed that $\sum_{i=1}^{n}\kappa_{i} \neq 0$.
### Checking if $x_{n}^{*} < x_{n+1}^{*}$
We assume that all nodes $\nu_{m}, m\leq n$ are static and placed at equilibriums so that $x_{m}^{*} < x_{m+1}^{*}\;\forall\;m<n$.
Now:
$$
\begin{aligned}
  x_{n}^{*} < x_{n+1}^{*}&\iff x_{n}^{*}<\frac{\sum_{i=1}^{n}\kappa_{i}(x_{i}^{*}+\xi_{n+1, i})}{\sum_{i=1}^{n}\kappa_{i}}\\
  &\iff x_{n}^{*}\sum_{i=1}^{n}\kappa_{i}<\sum_{i=1}^{n}\kappa_{i}(x_{i}^{*}+\xi_{n+1, i})\\
  &\iff x_{n}^{*}\sum_{i=1}^{n}\kappa_{i}-\sum_{i=1}^{n}\kappa_{i}x_{i}^{*}<\sum_{i=1}^{n}\kappa_{i}\xi_{n+1, i}\\
  &\iff \sum_{i=1}^{n}\kappa_{i}(x_{n}^{*}-x_{i}^{*})<\sum_{i=1}^{n}\kappa_{i}\xi_{n+1, i}\\
\end{aligned}
$$
In the left sum, the term $\kappa_{n}(x_{n}^{*}-x_{n}^{*}) = 0$, thus:
$$
\begin{aligned}
  x_{n}^{*} < x_{n+1}^{*}&\iff \sum_{i=1}^{n-1}\kappa_{i}(x_{n}^{*}-x_{i}^{*})<\sum_{i=1}^{n}\kappa_{i}\xi_{n+1, i}\\
\end{aligned}
$$
Seen as $x_{m}^{*} < x_{m+1}^{*}\;\forall\;m<n$, we know that $x_{m-i}^{*} < x_{m+1}^{*}\;\forall\;m<n, 0\leq i<m$. Thus we know that $x_{m+1}^{*} - x_{m-i}^{*} > 0\;\forall\;m<n, 0\leq i<m$. If we further assume that $\kappa_{i} \geq 0\;\forall\;0<i<n$, we have that:
$$
\begin{aligned}
 \sum_{i=1}^{n-1}\kappa_{i}(x_{n}^{*}-x_{i}^{*})\geq 0\\
\end{aligned}
$$
Thus:
$$
\begin{aligned}
  x_{n}^{*} < x_{n+1}^{*}&\iff 0\leq\sum_{i=1}^{n-1}\kappa_{i}(x_{n}^{*}-x_{i}^{*})<\sum_{i=1}^{n}\kappa_{i}\xi_{n+1, i}\\
  &\iff 0<\sum_{i=1}^{n}\kappa_{i}\xi_{n+1, i}\\
\end{aligned}
$$
$\xi_{n+1, i}\geq0 \;\forall\;0<i\leq n$ by design.
If we choose $\kappa_{i}\geq 0\;\forall\;0<i\leq n$ we have:

$$
\;\exist\;0<i\leq n:\kappa_{i} > 0, \xi_{n+1, i}>0\iff x_{n}^{*} < x_{n+1}^{*}
$$

> **Assumptions summary**
> 
> $\sum_{i=1}^{n}\kappa_{i} \neq 0$
>
>$\kappa_{i} \geq 0\;\forall\;0<i<n\implies\sum_{i=1}^{n-1}\kappa_{i} \geq 0$
>
>Thus
>
> $\sum_{i=1}^{n-1}\kappa_{i} = 0 \implies\sum_{i=1}^{n}\kappa_{i} = \kappa_{n}\neq 0$
>
> $\sum_{i=1}^{n-1}\kappa_{i} = \sum_{i=1}^{n-1}\kappa_{i}> 0 \implies\sum_{i=1}^{n}\kappa_{i} = \kappa_{n} + \sum_{i=1}^{n-1}\kappa_{i}\neq 0 \implies \kappa_{n}\neq-\sum_{i=1}^{n-1}\kappa_{i}$

## Extending to 2D

A node , $\nu_{n}$ now has state $\mathbf{x}_{n} = \begin{bmatrix}x_{n}&y_{n}\end{bmatrix}^{T}\in\mathbb{R}^{2}$. The RSSI is still just a scalar variable.
Due to thus the potential field for node $n+1$ is modified:
### Potential field for drone $\nu_{i+1}$
$$
U_{n+1} = \frac{1}{2}\sum_{i=1}^{n}\kappa_{i}||\mathbf{x}_{n+1}-\mathbf{x}_{i}-\mathbf{1}_{2\times1}\xi_{n+1,i}||^{2}
$$

### Force field affecting drone $\nu_{n+1}$
$$
\begin{aligned}
\mathbf{F}_{n+1} &= -\frac{\partial}{\partial \mathbf{x}_{n+1}}U_{n+1} = -\frac{1}{2}\sum_{i=1}^{n}\kappa_{i}\frac{\partial}{\partial \mathbf{x}_{n+1}}||\mathbf{x}_{n+1}-\mathbf{x}_{i}-\mathbf{1}_{2\times1}\xi_{n+1,i}||^{2}\\
&=-\sum_{i=1}^{n}\kappa_{i}(\mathbf{x}_{n+1}-\mathbf{x}_{i}-\mathbf{1}_{2\times1}\xi_{n+1,i})\\
&=\sum_{i=1}^{n}\kappa_{i}(\mathbf{x}_{i}-\mathbf{x}_{n+1}+\mathbf{1}_{2\times1}\xi_{n+1,i})\\
\end{aligned}
$$

### Equilibrium point for drone $\nu_{n+1}$

$$
\begin{aligned}
  \mathbf{x}_{n+1} = \mathbf{x}_{n+1}^{*}&\iff \mathbf{F}_{n+1} = \mathbf{0}\\
  &\iff  =\sum_{i=1}^{n}\kappa_{i}(\mathbf{x}_{i}-\mathbf{x}_{n+1}^{*}+\mathbf{1}_{2\times1}\xi_{n+1,i})=\mathbf{0}\\
  &\iff -\mathbf{x}_{n+1}^{*}\sum_{i=1}^{n}\kappa_{i} + \sum_{i=1}^{n}\kappa_{i}(\mathbf{x}_{i}+\mathbf{1}_{2\times1}\xi_{n+1,i})=\mathbf{0}\\
  &\iff \mathbf{x}_{n+1}^{*} = \frac{\sum_{i=1}^{n}\kappa_{i}(\mathbf{x}_{i}+\mathbf{1}_{2\times1}\xi_{n+1,i})}{\sum_{i=1}^{n}\kappa_{i}}\\
\end{aligned}
$$

### Checking if $||\mathbf{x}_{n}^{*}|| < ||\mathbf{x}_{n+1}^{*}||$

We assume that all nodes $\nu_{m}, m\leq n$ are static and placed at equilibriums so that $||\mathbf{x}_{m}^{*}|| < ||\mathbf{x}_{m+1}^{*}||\;\forall\;m<n$.
Now:
$$
\begin{aligned}
||\mathbf{x}_{n}^{*}|| < ||\mathbf{x}_{n+1}^{*}||&\iff||\mathbf{x}_{n}^{*}|| < \Bigg|\Bigg|\frac{\sum_{i=1}^{n}\kappa_{i}(\mathbf{x}_{i}+\mathbf{1}_{2\times1}\xi_{n+1,i})}{\sum_{i=1}^{n}\kappa_{i}}\Bigg|\Bigg|\\
&\iff||\mathbf{x}_{n}^{*}||\Big|\Big|\sum_{i=1}^{n}\kappa_{i}\Big|\Big| = ||\mathbf{x}_{n}^{*}||\Big|\sum_{i=1}^{n}\kappa_{i}\Big| < \Big|\Big|\sum_{i=1}^{n}\kappa_{i}(\mathbf{x}_{i}+\mathbf{1}_{2\times1}\xi_{n+1,i})\Big|\Big|\\
&\iff||\mathbf{x}_{n}^{*}||\Big|\sum_{i=1}^{n}\kappa_{i}\Big| < \Big|\Big|\sum_{i=1}^{n}\kappa_{i}(\mathbf{x}_{i}+\mathbf{1}_{2\times1}\xi_{n+1,i})\Big|\Big|\leq \Big|\Big|\sum_{i=1}^{n}\kappa_{i}\mathbf{x}_{i}\Big|\Big|+\Big|\Big|\sum_{i=1}^{n}\kappa_{i}\mathbf{1}_{2\times1}\xi_{n+1,i}\Big|\Big|\\
&\iff||\mathbf{x}_{n}^{*}||\Big|\sum_{i=1}^{n}\kappa_{i}\Big| - \Big|\Big|\sum_{i=1}^{n}\kappa_{i}\mathbf{x}_{i}\Big|\Big| < \Big|\Big|\sum_{i=1}^{n}\kappa_{i}\mathbf{1}_{2\times1}\xi_{n+1,i}\Big|\Big|\\
&\iff||\mathbf{x}_{n}^{*}||\Big|\sum_{i=1}^{n}\kappa_{i}\Big| - \sum_{i=1}^{n}|\kappa_{i}|\cdot||\mathbf{x}_{i}|| \leq \Big|\Big|\sum_{i=1}^{n}\kappa_{i}\mathbf{x}_{n}^{*}\Big|\Big| - \Big|\Big|\sum_{i=1}^{n}\kappa_{i}\mathbf{x}_{i}\Big|\Big| < \Big|\Big|\sum_{i=1}^{n}\kappa_{i}\mathbf{1}_{2\times1}\xi_{n+1,i}\Big|\Big|\\
\end{aligned}
$$
Now if we choose $\kappa_{i}\geq0\;\forall\;0<i\leq n$ we have $|\kappa_{i}| = \kappa_{i}\;\forall\;0<i\leq n$ and thus:
$$
\Big|\sum_{i=1}^{n}\kappa_{i}\Big| = \sum_{i=1}^{n}|\kappa_{i}| = \sum_{i=1}^{n}\kappa_{i}
$$
This gives:
$$
\begin{aligned}
||\mathbf{x}_{n}^{*}|| < ||\mathbf{x}_{n+1}^{*}||&\iff||\mathbf{x}_{n}^{*}||\sum_{i=1}^{n}\kappa_{i} - \sum_{i=1}^{n}\kappa_{i}||\mathbf{x}_{i}|| \leq \Big|\Big|\sum_{i=1}^{n}\kappa_{i}\mathbf{x}_{n}^{*}\Big|\Big| - \Big|\Big|\sum_{i=1}^{n}\kappa_{i}\mathbf{x}_{i}\Big|\Big| < \Big|\Big|\sum_{i=1}^{n}\kappa_{i}\mathbf{1}_{2\times1}\xi_{n+1,i}\Big|\Big|\\
&\iff\sum_{i=1}^{n-1}\kappa_{i}\big(||\mathbf{x}_{n}^{*}|| - ||\mathbf{x}_{i}^{*}||) < \Big|\Big|\sum_{i=1}^{n}\kappa_{i}\mathbf{1}_{2\times1}\xi_{n+1,i}\Big|\Big|\\
\end{aligned}
$$
As stated before we know that $||\mathbf{x}_{m}^{*}|| < ||\mathbf{x}_{m+1}^{*}||\;\forall\;m<n$. Thus $||\mathbf{x}_{m+1}^{*}|| - ||\mathbf{x}_{m-i}^{*}|| > 0\;\forall\;m<n,0<i<n$. Using the we have:
$$
\begin{aligned}
||\mathbf{x}_{n}^{*}|| < ||\mathbf{x}_{n+1}^{*}||&\iff0\leq\sum_{i=1}^{n-1}\kappa_{i}\big(||\mathbf{x}_{n}^{*}|| - ||\mathbf{x}_{i}^{*}||) < \Big|\Big|\sum_{i=1}^{n}\kappa_{i}\mathbf{1}_{2\times1}\xi_{n+1,i}\Big|\Big|\\
&\iff0 < \Big|\Big|\sum_{i=1}^{n}\kappa_{i}\mathbf{1}_{2\times1}\xi_{n+1,i}\Big|\Big| = \sum_{i=1}^{n}|\kappa_{i}|\cdot||\mathbf{1}_{2\times1}||\cdot|\xi_{n+1,i}| = \sqrt{2}\sum_{i=1}^{n}\kappa_{i}\xi_{n+1,i} \\
&\iff0<\sum_{i=1}^{n}\kappa_{i}\xi_{n+1,i}
\end{aligned}
$$

$\xi_{n+1, i}\geq0 \;\forall\;0<i\leq n$ by design.
If we choose $\kappa_{i}\geq 0\;\forall\;0<i\leq n$ we have:

$$
\;\exist\;0<i\leq n:\kappa_{i} > 0, \xi_{n+1, i}>0\iff ||\mathbf{x}_{n}^{*}|| < ||\mathbf{x}_{n+1}^{*}||
$$