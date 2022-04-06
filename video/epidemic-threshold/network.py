import numpy
from manim import *
from epydemic import SIR, SIR_FixedRecovery, ERNetwork
from epydemic_signals import StochasticSignalDynamics, SignalGenerator


class SingleSeedSIR(SIR_FixedRecovery):
    '''An SIR model with exactly one node initially seeded.'''

    def build(self, params):
        params[self.P_INFECTED] = 0.0
        super().build(params)

    def initialCompartments(self):
        '''Infect exactly one node, chosen at random.'''
        g = self.network()
        ns = set(g.nodes())
        N = len(ns)

        # choose one node and infect it
        rng = numpy.random.default_rng()
        n = rng.integers(N)
        self.changeInitialCompartment(n, self.INFECTED)

        # mark all other nodes as susceptible
        ns.remove(n)
        for n in ns:
            self.changeInitialCompartment(n, self.SUSCEPTIBLE)


class SIRVisualiser(SignalGenerator):
    '''A "signal generator" that creates a visualisation of the progress
    of an epidemic across a network.'''

    def __init__(self, scene):
        super().__init__(None)

        self._scene = scene

        self.addEventTypeHandler(SIR.INFECTED, self.infect)
        self.addEventTypeHandler(SIR.REMOVED, self.remove)

    def setUp(self, g, params):
        self.signal().setNetwork(g)
        m = self.experiment().process()
        self._graph = Graph.from_networkx(g, layout='spring', layout_scale=3)
        for n in g.nodes():
            if m.getCompartment(n) == SIR_FixedRecovery.SUSCEPTIBLE:
                c = self._scene._s_colour
            elif m.getCompartment(n) == SIR_FixedRecovery.INFECTED:
                c = self._scene._i_colour
            else:
                c = GREY
            self._graph[n].scale(self._scene._scale).set_color(c).set_fill(c).set_fill_opacity(1.0)
        self._scene.play(Create(self._graph))

    def infect(self, t, e):
        (n, _) = e
        self._scene.play(self._graph[n].animate.set_color(self._scene._i_colour).set_fill(self._scene._i_colour),
                         run_time=self._scene._delay)

    def remove(self, t, n):
        self._scene.play(self._graph[n].animate.set_color(self._scene._r_colour).set_fill(self._scene._r_colour),
                         run_time=self._scene._delay)


class Network(Scene):
    '''A scene showing a (small) SIR epidemic with fixed-time recovery on a (small) network.'''

    rng = numpy.random.default_rng()


    def begin(self, N, kmean, pInfect, tRemove = 1.0,
              delay = 1.0, scale = 2, s_colour = GREEN, i_colour = RED, r_colour = BLUE):
        self._delay = delay
        self._scale = scale
        self._s_colour = s_colour
        self._i_colour = i_colour
        self._r_colour = r_colour

        self._params = dict()
        self._params[ERNetwork.N] = N
        self._params[ERNetwork.KMEAN] = kmean
        self._params[SIR_FixedRecovery.P_INFECT] = pInfect
        self._params[SIR_FixedRecovery.T_INFECTED] = tRemove
        self._e = StochasticSignalDynamics(SingleSeedSIR(), ERNetwork())
        self._e.addSignalGenerator(SIRVisualiser(self))

    def run(self):
        rc = self._e.set(self._params).run(fatal=True)

    def construct(self):
        N = 10
        kmean = 5
        pInfect = 0.9
        tRemove = 2.0
        delay = 1.0

        self.begin(N, kmean, pInfect, tRemove, delay)
        self.run()

        self.wait(5)
