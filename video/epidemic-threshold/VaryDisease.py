import numpy
from manim import *
from epydemic import SIR, SIR_FixedRecovery, ERNetwork
from epydemic_signals import StochasticSignalDynamics, SignalGenerator
import sys
sys.path.append('.')
from Network import Network


class VaryDisease(Network):

    def again(self, pInfect, tRemove = 1.0):
        self._params[SIR_FixedRecovery.P_INFECT] = pInfect
        self._params[SIR_FixedRecovery.T_INFECTED] = tRemove

    def construct(self):
        N = 10
        kmean = 5
        pInfectLow = 0.2
        pInfectHigh = 1.0
        tRemoveLow = 2.0
        tRemoveHigh = 4.0
        delay = 1.0

        # build a fixed network on which to run the epidemic
        params = dict()
        params[ERNetwork.N] = N
        params[ERNetwork.KMEAN] = kmean
        g = ERNetwork().set(params).generate()

        n_var = Variable(N, MathTex('N'), num_decimal_places=0)
        k_var = Variable(kmean, MathTex('\langle k \\rangle'), num_decimal_places=0).next_to(n_var, DOWN).align_to(n_var, LEFT, alignment_vect=RIGHT)
        p_var = Variable(pInfectLow, MathTex('p_{infect}', num_decimal_places=2)).next_to(k_var, DOWN).align_to(n_var, LEFT, alignment_vect=RIGHT)
        t_var = Variable(tRemoveLow, MathTex('t_{remove}', num_decimal_places=2).next_to(p_var, DOWN).align_to(p_var, LEFT, alignment_vect=RIGHT))
        metrics = VGroup(n_var, k_var, p_var, t_var)
        metrics.shift(2 * RIGHT + (metrics.height / 2) * UP)
        self.play(Write(metrics))

        self.begin(N, kmean, pInfectLow, tRemoveLow, g, delay=delay)
        self.run()

        self.again(pInfectHigh, tRemoveHigh)
        self.play(p_var.tracker.animate.set_value(pInfectHigh),
                  t_var.tracker.animate.set_value(tRemoveHigh))
        self.run()
        self.play(FadeOut(metrics))

        self.wait(5)
