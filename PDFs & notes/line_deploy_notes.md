
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