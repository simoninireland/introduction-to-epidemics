import numpy
from manim import *
from epydemic import SIR, ERNetwork
from epyc import HDF5LabNotebook, Experiment
from pandas import DataFrame


class FocussedRawAndError(Scene):

    def construct(self):
        nb = HDF5LabNotebook('src/datasets/epidemic-threshold.h5')
        nb.select('er-network-focus')
        df = nb.dataframe()

        pInfects = numpy.sort(df[SIR.P_INFECT].unique())
        pInfectsRange = pInfects.max()   # run from 0.0 up
        dp = abs(int(numpy.log10(pInfectsRange))) + 1
        pInfectsRounded = round(pInfectsRange, dp)
        pInfectsStep = pInfectsRounded / 10

        ax = Axes(x_range=[0.0, pInfects.max(), pInfectsStep],
                  y_range=[0.0, 1.0, 0.1],
                  axis_config={'color': GREEN,
                               'include_numbers': True,
                               'decimal_number_config': {'num_decimal_places': 1},
                               'font_size': 24,
                               'include_tip': False},
                  x_axis_config={'decimal_number_config': {'num_decimal_places': dp + 1}},
                  y_axis_config={'decimal_number_config': {'num_decimal_places': 1}},)
        labels = VGroup(ax.get_x_axis_label('p_{infect}'),
                        ax.get_y_axis_label('S'))

        means, stds, dots = [], [], []
        for pInfect in pInfects:
            dfp = df[df[SIR.P_INFECT] == pInfect]
            rs = dfp[SIR.REMOVED] / dfp[ERNetwork.N]
            mean, std = rs.mean(), rs.std()
            means.append(mean)
            stds.append(std)
            for r in rs:
                dots.append(Dot(ax.coords_to_point(pInfect, r), radius=0.05,
                                color=RED, fill_opacity=0.4))

        graph = ax.plot_line_graph(x_values=pInfects, y_values=means,
                                   line_color=RED, stroke_width=4,  add_vertex_dots=False)

        smoothStds = [0] + [(stds[i - 1] + stds[i] + stds[i + 1]) / 3 for i in range(1, len(stds) - 1)] + [0]
        smoothStds = stds

        vertices = [ax.c2p(pInfects[i], means[i] - smoothStds[i]) for i in range(len(pInfects))] + [ax.c2p(pInfects[i], means[i] + smoothStds[i]) for i in reversed(range(len(pInfects)))]
        errorRegion = Polygon(*vertices, color=PINK, fill_color=PINK, fill_opacity=0.3)

        self.play(Create(ax, run_time=2), Create(labels, run_time=2))
        self.play(Create(errorRegion, run_time=3))
        # self.play(ShowIncreasingSubsets(VGroup(*dots), run_time=3))
        # self.play(Create(graph))



        self.wait(5)
