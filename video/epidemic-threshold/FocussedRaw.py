import numpy
from manim import *
from epydemic import SIR, ERNetwork
from epyc import HDF5LabNotebook, Experiment


class FocussedRaw(Scene):

    def construct(self):
        nb = HDF5LabNotebook('src/datasets/epidemic-threshold.h5')
        nb.select('er-network-focus')
        df = nb.dataframe()

        pInfects = df[SIR.P_INFECT].unique()
        pInfectsRange = pInfects.max()   # run from 0.0 up
        dp = abs(int(numpy.log10(pInfectsRange))) + 1
        pInfectsRounded = round(pInfectsRange, dp)
        pInfectsStep = pInfectsRounded / 10

        ax = Axes(x_range=[pInfects.min(), pInfects.max(), pInfectsStep],
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

        dots = []
        stride = 5
        for pInfect in pInfects:
            dfp = df[df[SIR.P_INFECT] == pInfect]
            rs = dfp[SIR.REMOVED][::stride] / dfp[ERNetwork.N][::stride]
            for r in rs:
                dots.append(Dot(ax.coords_to_point(pInfect, r), radius=0.05, color=RED))
        dotsGroup = VGroup(*dots)

        self.play(Create(ax, run_time=2), Create(labels, run_time=2))
        self.play(ShowIncreasingSubsets(dotsGroup, run_time=3))


        self.wait(5)
