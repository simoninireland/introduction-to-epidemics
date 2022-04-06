import numpy
from networkx import average_neighbor_degree
from manim import *


class Topology(Scene):
    '''A scene showing how we can wire the same nodes in different
    ways, and the changes this has on the key metrics.'''

    rng = numpy.random.default_rng()

    def newEdge(self, es):
        e1 = None
        while e1 is None:
            n1 = self.rng.integers(len(es))
            m1 = None
            while m1 is None:
                i = self.rng.integers(len(es))
                if i != n1:
                    m1 = i
            if (n1, m1) not in es and (m1, n1) not in es:
                e1 = (n1, m1)
        return e1

    def replace(self, es, e):
        (n, m) = e
        e1 = None
        while e1 is None:
            n1 = None
            while n1 is None:
                i = self.rng.integers(len(es))
                if i != n:
                    n1 = i
            m1 = None
            while m1 is None:
                i = self.rng.integers(len(es))
                if i != m and i != n1:
                    m1 = i
            if (n1, m1) not in es and (m1, n1) not in es:
                e1 = (n1, m1)
        return e1

    def rewireEdges(self, es, nEdges):
        for _ in range(nEdges):
            i = self.rng.integers(len(es))
            es[i] = self.replace(es, es[i])
        return es

    def addEdges(self, es, nEdges):
        for _ in range(nEdges):
            es.append(self.newEdge(es))
        return es

    @staticmethod
    def meandegree(g):
        return numpy.mean(list(dict(g.degree()).values()))

    @staticmethod
    def maxdegree(g):
        return max(list(dict(g.degree()).values()))

    def construct(self):
        N = 10

        nodes = list(range(N))
        line = {n: [n - (N / 2), 0.0, 0.0] for n in nodes}

        g = Graph(vertices=nodes, edges=[], layout=line, layout_scale=2).shift(LEFT)
        self.play(Create(g))
        self.wait(1)

        n = Variable(N, MathTex('N'), num_decimal_places=0)
        m = Variable(N, MathTex('M'), num_decimal_places=0).next_to(n, DOWN).align_to(n, LEFT, alignment_vect=RIGHT)
        kmean = Variable(0, MathTex('\langle k \\rangle'), num_decimal_places=2).next_to(m, DOWN).align_to(n, LEFT, alignment_vect=RIGHT)
        kmax = Variable(0, MathTex('k_{max}'), num_decimal_places=0).next_to(kmean, DOWN).align_to(n, LEFT, alignment_vect=RIGHT)
        metrics = VGroup(n, m, kmean, kmax)
        metrics.shift((metrics.height / 2)* UP + 4.0 * RIGHT)
        self.play(Write(metrics))
        self.wait(1)

        es = [(n, (n + 1) % N) for n in nodes]
        self.play(g.animate.add_edges(*es),
                  m.tracker.animate.set_value(len(g._graph.edges())),
                  kmean.tracker.animate.set_value(self.meandegree(g._graph)),
                  kmax.tracker.animate.set_value(self.maxdegree(g._graph)))
        self.wait(1)

        self.play(g.animate.change_layout('circular'))
        self.wait(1)

        self.play(g.animate.remove_edges(*es),
                  m.tracker.animate.set_value(len(g._graph.edges())),
                  kmean.tracker.animate.set_value(self.meandegree(g._graph)),
                  kmax.tracker.animate.set_value(self.maxdegree(g._graph)))
        self.wait(1)
        es = self.rewireEdges(es, int(N / 2))
        self.play(g.animate.add_edges(*es),
                  m.tracker.animate.set_value(len(g._graph.edges())),
                  kmean.tracker.animate.set_value(self.meandegree(g._graph)),
                  kmax.tracker.animate.set_value(self.maxdegree(g._graph)))
        self.wait(1)

        es = self.addEdges(es, N)
        self.play(g.animate.add_edges(*es),
                  m.tracker.animate.set_value(len(g._graph.edges())),
                  kmean.tracker.animate.set_value(self.meandegree(g._graph)),
                  kmax.tracker.animate.set_value(self.maxdegree(g._graph)))
        self.wait(1)




        self.wait(5)
