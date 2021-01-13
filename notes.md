# Notes from Optimality Analysis of Sensor-Target Localization Geometries
## Definition of Problem 3
Assume there exists a set of $N \geq 3$ time-of-arrival measurements from $N$ spatially distinct sensors.
Using the observable set of random timing measurements 
$\hat{\mathbf{y}}\sim\mathcal{N}(\mathbf{y}(\mathbf{x}), \sigma_{t}^{2}\mathbf{I}_{N})$, find an estimate $\tilde{\mathbf{x}}$
of the true event location $\mathbf{x}$ which
includes both the event location $\mathbf{p}$ and the time of the event $\tau$.

> ### Remark
> If the expected value of the estimate $E[\tilde{\mathbf{p}}]$ ($E[\tilde{\mathbf{x}}]$) is constrained to be $\mathbf{p}$, then 
Problem 3 is one of unbiased localization.
## Metric for optimal sensor placement
> ### Nomenclature
> Target emitter positioned at $\mathbf{p} = [x_{p}, y_{p}]$ transmitts signal at time $\tau$. Denoting this information by $\mathbf{x} = [x_{p}, y_{p}, \tau]^{T}$.
> 
> Sensor $i$ positioned at $\mathbf{s}_{i} = [x_{i}, y_{i}]^{T}$.
> 
> $t_{i}(\cdot)$ denotes the signal time-of-arrival at sensor $i$, and is calculated as $t_{i}(\mathbf{x}) = \frac{||\mathbf{p}-\mathbf{s}_{i}||}{v} + \tau$, where $\mathbf{x} = [\mathbf{p}^{T} \tau]^{T}$, and $v$ is the propagation speed of the signal.

The measured ToA is in general noisey. It is assumed that all ToA measurements are corrupted by white Gaussian noise with variance $\sigma_{t}$. Thus a signle ToA measurement at sensor $i$ takes the form:
> $\hat{t}_{i}(\mathbf{x}) = t_{i}(\mathbf{x}) + e_{i}$, $e_{i}\sim\mathcal{N}(0, \sigma_{t})$

Gathering ToA measurements from all sensors $i\in\mathcal{S} = \{0\dots N-1\}$ in a vector $\hat{\mathbf{y}}(\cdot)$:
> $\hat{\mathbf{y}}(\mathbf{x}) = [t_{0}(\mathbf{x})\dots t_{N-1}(\mathbf{x})]^{T} + [e_{0}\dots e_{N-1}]^{T} = \mathbf{y}(\mathbf{x}) + \mathbf{e}$

It is assumed that $\hat{\mathbf{y}}(\mathbf{x})\sim\mathcal{N}(\mathbf{y}(\mathbf{x}), \sigma_{t}\mathbf{I}_{N})$, i.e. no correlation between ToA measurements.

The likelihood function of $\mathbf{x}$ given the measurement vector $\hat{\mathbf{y}}\sim\mathcal{N}(\mathbf{y}(\mathbf{x}), \sigma_{t}\mathbf{I}_{N})$ is given by:
> $f_{\hat{\mathbf{y}}}(\hat{\mathbf{y}}; \mathbf{x}) = \frac{1}{(2\pi)^{N/2}|\sigma_{t}\mathbf{I}_{N}|^{1/2}}\exp{\big(-\frac{1}{2}(\hat{\mathbf{y}}-\mathbf{y}(\mathbf{x}))^{T}(\sigma_{t}\mathbf{I}_{N})^{-1}(\hat{\mathbf{y}}-\mathbf{y}(\mathbf{x}))\big)}$

In general, the Cramer-Rao inequality lower bounds the *covariance* acheivable by an unbiased estimator (under two mild regularity conditions). For an *unbiased* estimates $\tilde{\mathbf{x}}$ of $\mathbf{x}$, The Cramer-Rao bound states that:
> $E[(\tilde{\mathbf{x}}-\mathbf{x})(\tilde{\mathbf{x}}-\mathbf{x})^{T}]\geq \mathcal{I}(\mathbf{x})^{-1} := \mathcal{C}(\mathbf{x})$

If the statement above holds with equality, the estimator is *efficient* and the parameter estimate $\tilde{\mathbf{x}}$ is unique.

Under the assumption of Gaussian measurement errors and errors being independent of the parameter, the Fisher information matrix is given by
> $\mathcal{I}(\mathbf{x}) = \nabla_{\mathbf{x}}\mathbf{y}(\mathbf{x})^{T}(\sigma_{t}\mathbf{I}_{N})^{-1}\nabla_{\mathbf{x}}\mathbf{y}(\mathbf{x})$, where $\nabla_{\mathbf{x}}\mathbf{y}(\mathbf{x})$ is the gradient of $\mathbf{y}$ wrt. $\mathbf{x}$.

> ### Remark
> $\mathcal{C}(\mathbf{x}) = \mathcal{I}(\mathbf{x})^{-1}$ is symmetric positive definite given that $\mathcal{I}(\cdot)$ is invertible, and defines an *uncertainty ellipsoid*. Denote the eigenvalues of $\mathcal{C}(\mathbf{x})$ by $\lambda_{i}$, $i = 0, 1, 2$. Note that $\sqrt{\lambda_{i}}$, $i = 0, 1, 2$ is the length of the $i^{\mathrm{th}}$ axis of the ellipsoid. Note also that the axes lie along the corresponding eigenvectors of $\mathcal{C}(\mathbf{x})$.

A scalar functional measure of the ‘size’ of the
uncertainty ellipse provides a useful characterization of the potential performance of an unbiased estimator. For computational purposes the determinant of the Fisher information matrix, $\det(\mathcal{I}(\mathbf{x}))$, is used as a computationally feasible measure of the volume of the uncertainty ellipsoid.

> ### Tip
> Check out "D-optimal experimental design"

