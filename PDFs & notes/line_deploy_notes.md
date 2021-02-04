
### Potential field affecting drone $\nu_{n+1}$
$$
U_{n+1} = \frac{1}{2}\sum_{i=1}^{n}\kappa_{i}||x_{n+1}-x_{i}-\xi_{n+1,i}||^{2}
$$
### Force field affecting drone $\nu_{n+1}$
$$
\begin{aligned}
F_{n+1} &= \frac{\partial}{\partial x_{n+1}}U_{n+1} = \frac{1}{2}\sum_{i=1}^{n}\kappa_{i}\frac{\partial}{\partial x_{n+1}}||x_{n+1}-x_{i}-\xi_{n+1,i}||^{2}\\
&=\frac{1}{2}\sum_{i=1}^{n}\kappa_{i}\frac{\partial}{\partial x_{n+1}}(x_{n+1}-x_{i}-\xi_{n+1,i})^{2}\\
&=\frac{1}{2}\sum_{i=1}^{n}\kappa_{i}2(x_{n+1}-x_{i}-\xi_{n+1,i})\frac{\partial}{\partial x_{n+1}}(x_{n+1}-x_{i}-\xi_{n+1,i})\\
&=\sum_{i=1}^{n}\kappa_{i}(x_{n+1}-x_{i}-\xi_{n+1,i})\\
\end{aligned}
$$

### Equilibrium point for drone $\nu_{n+1}$
$$
\begin{aligned}
  F_{n+1} = 0&\iff\sum_{i=1}^{n}\kappa_{i}(x_{n+1}-x_{i}-\xi_{n+1,i})=0\\
  &\iff x_{n+1}\sum_{i=1}^{n}\kappa_{i} - \sum_{i=1}^{n}\kappa_{i}(x_{i}+\xi_{n+1, i}) = 0\\
  &\iff x_{n+1} = \frac{\sum_{i=1}^{n}\kappa_{i}(x_{i}+\xi_{n+1, i})}{\sum_{i=1}^{n}\kappa_{i}}\\

\end{aligned}
$$
### Checking if $x_{n+1} > x_{n}$
$$
\begin{aligned}
  x_{n+1}>x_{n}\iff&\frac{\sum_{i=1}^{n}\kappa_{i}(x_{i}+\xi_{n+1, i})}{\sum_{i=1}^{n}\kappa_{i}} > x_{n}\\
  \iff&\sum_{i=1}^{n}\kappa_{i}(x_{i}+\xi_{n+1, i}) > x_{n}\sum_{i=1}^{n}\kappa_{i}\\
  \iff&x_{n}\kappa_{n}+\sum_{i=1}^{n-1}\kappa_{i}x_{i}+\sum_{i=1}^{n}\kappa_{i}\xi_{n+1, i} > x_{n}\sum_{i=1}^{n}\kappa_{i}\\
  \iff&\sum_{i=1}^{n-1}\kappa_{i}x_{i}+\sum_{i=1}^{n}\kappa_{i}\xi_{n+1, i} > x_{n}\Big(\sum_{i=1}^{n}[\kappa_{i}] - \kappa_{n}\Big)\\
\end{aligned}
$$
Choosing $\kappa_{n}\leq\sum_{i=1}^{n}\kappa_{i}$ yields:
$$
\sum_{i=1}^{n-1}\kappa_{i}x_{i}+\sum_{i=1}^{n}\kappa_{i}\xi_{n+1, i} > 0
$$
By design $\xi_{n, i} > 0\;\forall\;n,i$. If the origin of the coordinate system is situated at the first node ($\nu_{1}$ AKA the SCS), 
we have for the two first nodes, $\nu_{1}$ and $\nu_{2}$:
$$
\sum_{i=1}^{1-1}\kappa_{i}x_{i}+\sum_{i=1}^{1}\kappa_{i}\xi_{1+1, i} = \kappa_{1}\xi_{2, 1} > 0.
$$
Thus we have $x_{2} > x_{1} = 0$.

Assume $x_{n} > x_{n-1}\;\forall\;n<m$. Thus:
$$
\sum_{i=1}^{n-2}\kappa_{i}x_{i}+\sum_{i=1}^{n-1}\kappa_{i}\xi_{n, i} > 0.
$$
For $m = n+1$ we have:
$$
\sum_{i=1}^{m-1}\kappa_{i}x_{i}+\sum_{i=1}^{m}\kappa_{i}\xi_{m+1, i}
$$
We know that $x_{n} > x_{n-1}\;\forall\;n<m$, and that $x_{1} = 0$. Thus we know that $x_{n} > 0\;\forall\;n<m$. Thus:
$$
\sum_{i=1}^{m-1}\kappa_{i}x_{i}+\sum_{i=1}^{m}\kappa_{i}\xi_{m+1, i} = \sum_{i=1}^{n}\kappa_{i}x_{i}+\sum_{i=1}^{m}\kappa_{i}\xi_{m+1, i} > \sum_{i=1}^{m}\kappa_{i}\xi_{m+1, i}>0
$$
And we conclude that $x_{m} = x_{n+1} > x_{n}$.