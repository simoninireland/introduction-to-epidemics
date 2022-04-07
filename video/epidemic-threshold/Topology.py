import numpy
from manim import *


class Topology(Scene):
    '''A scene showing how we can wire the same nodes in different
    ways, and the changes this has on the key metrics.'''

    rng = numpy.random.default_rng()

    def newEdge(self, es, N):
        '''Create a new edge, not a self-loop and not in es.'''
        e1 = None
        while e1 is None:
            n1 = self.rng.integers(N)
            m1 = None
            while m1 is None:
                i = self.rng.integers(N)
                if i != n1:
                    m1 = i
            if (n1, m1) not in es and (m1, n1) not in es:
                e1 = (n1, m1)
        return e1

    def replace(self, es, e, N):
        '''Replace the given edge with a new edge, not a self-loop and not parallel.'''
        (n, m) = e
        e1 = None
        while e1 is None:
            n1 = None
            while n1 is None:
                i = self.rng.integers(N)
                if i != n:
                    n1 = i
            m1 = None
            while m1 is None:
                i = self.rng.integers(N)
                if i != m and i != n1:
                    m1 = i
            if (n1, m1) not in es and (m1, n1) not in es:
                e1 = (n1, m1)
        return e1

    def rewireEdges(self, es, N, nEdges):
        '''Re-wire some of the edges in es.'''
        for _ in range(nEdges):
            i = self.rng.integers(len(es))
            es[i] = self.replace(es, es[i], N)
        return es

    def addEdges(self, es, N, nEdges):
        '''Add new edges to es.'''
        for _ in range(nEdges):
            es.append(self.newEdge(es, N))
        return es

    @staticmethod
    def meandegree(g):
        '''Helper method for global mean degree, mysteriously missing from networkx.'''
        return numpy.mean(list(dict(g.degree()).values()))

    @staticmethod
    def maxdegree(g):
        '''Helper method for global maximum degree, mysteriously missing from networkx.'''
        return max(list(dict(g.degree()).values()))

    def construct(self):
        N = 10

        nodes = list(range(N))
        line = {n: [n - (N / 2), 0.0, 0.0] for n in nodes}

        g = Graph(vertices=nodes, edges=[], layout=line, layout_scale=2).shift(LEFT)
        self.play(Create(g))
        self.wait(1)

        # block of text with topological parameters
        n = Variable(N, MathTex('N'), num_decimal_places=0)
        m = Variable(N, MathTex('M'), num_decimal_places=0).next_to(n, DOWN).align_to(n, LEFT, alignment_vect=RIGHT)
        kmean = Variable(0, MathTex('\langle k \\rangle'), num_decimal_places=2).next_to(m, DOWN).align_to(n, LEFT, alignment_vect=RIGHT)
        kmax = Variable(0, MathTex('k_{max}'), num_decimal_places=0).next_to(kmean, DOWN).align_to(n, LEFT, alignment_vect=RIGHT)
        metrics = VGroup(n, m, kmean, kmax)
        metrics.shift((metrics.height / 2) * UP + 4.0 * RIGHT)
        self.play(Write(metrics))
        self.wait(1)

        # add edges to create a circle
        es = [(n, (n + 1) % N) for n in nodes]
        self.play(g.animate.add_edges(*es),
                  m.tracker.animate.set_value(len(g._graph.edges())),
                  kmean.tracker.animate.set_value(self.meandegree(g._graph)),
                  kmax.tracker.animate.set_value(self.maxdegree(g._graph)))
        self.wait(1)

        # change layout to make edges visible
        self.play(g.animate.change_layout('circular'))
        self.wait(1)

        # remove all edges
        self.play(g.animate.remove_edges(*es),
                  m.tracker.animate.set_value(len(g._graph.edges())),
                  kmean.tracker.animate.set_value(self.meandegree(g._graph)),
                  kmax.tracker.animate.set_value(self.maxdegree(g._graph)))
        self.wait(1)

        # rewire half the edges randomly
        es = self.rewireEdges(es, int(N / 2), N)
        self.play(g.animate.add_edges(*es),
                  m.tracker.animate.set_value(len(g._graph.edges())),
                  kmean.tracker.animate.set_value(self.meandegree(g._graph)),
                  kmax.tracker.animate.set_value(self.maxdegree(g._graph)))
        self.wait(1)

        # add more random edges
        self.play(g.animate.remove_edges(*es),
                  kmean.tracker.animate.set_value(self.meandegree(g._graph)),
                  kmax.tracker.animate.set_value(self.maxdegree(g._graph)))
        es = self.addEdges(es, N, N)
        self.play(g.animate.add_edges(*es),
                  m.tracker.animate.set_value(len(g._graph.edges())),
                  kmean.tracker.animate.set_value(self.meandegree(g._graph)),
                  kmax.tracker.animate.set_value(self.maxdegree(g._graph)))
        self.wait(1)

        # star topology
        self.play(g.animate.remove_edges(*es),
                  m.tracker.animate.set_value(len(g._graph.edges())),
                  kmean.tracker.animate.set_value(self.meandegree(g._graph)),
                  kmax.tracker.animate.set_value(self.maxdegree(g._graph)))
        star_es = [(0, n) for n in range(1, N)]
        self.play(g.animate.add_edges(*star_es),
                  g.animate.change_layout('spring'),
                  m.tracker.animate.set_value(len(g._graph.edges())),
                  kmean.tracker.animate.set_value(self.meandegree(g._graph)),
                  kmax.tracker.animate.set_value(self.maxdegree(g._graph)))

        self.wait(5)
