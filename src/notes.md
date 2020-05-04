# Notes

## The simplest model

(note:beta)=
[1] In the computational epidemiology and network science literatures the
parameter we've called $p_{\mathit{infect}}$ is usually denoted
$\beta$, while $p_{remove}$ is denoted $\alpha$. It's easier to
understand what's going on if we spell the meaning of the symbols out.

(note:euler)=
[2] This approach to integration to get a time series, known as the
*direct* or *Euler* method, isn't safe in general, as it risks falling
foul of numerical instability in the equations. There are several more
robust solutions for the more complex cases, notably the Runge-Kutta
methods that are built into Python's `scipy` library.

(note:ode)=
[3] We've engaged in some mathematical sleight-of-hand here, in that what
we've described as a *discrete* model (of people being susceptible,
infected, and so on) has then be treated as a *continuous* model that
represents the sizes of compartments as real numbers. In order to work
in this way the three SIR equations should really be be phrased as
*differential* equations rather than as *difference* equations so that
the passage from discrete to continuous time makes mathematical
sense. The results obtained are the same in both cases, however.


## Connectivity

(note:chickenpox)=
[1] In chickenpox the infected individual &ndash; almost always a
child &ndash; is latent for 7–10 days after exposure, but only
infectious for about 24 hours before the symptoms (an itchy rash)
appear.

