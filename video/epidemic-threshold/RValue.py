import numpy
from manim import *


class RValue(Scene):
    '''A scene showing the progression of a contact tree.'''

    rng = numpy.random.default_rng()


    def begin(self, R, fan, levels,
              s_colour = GREEN, i_colour = RED,
              radius = 0.2, level_width = 2.0, sibling_spacing = 0.2, level_spacing = 1.0):
        # overall parameters
        self._R = R
        self._fan = fan
        self._levels = levels
        self._s_colour = s_colour
        self._i_colour = i_colour
        self._radius = radius
        self._level_width = level_width
        self._sibling_spacing = sibling_spacing
        self._level_spacing = level_spacing

        # running state
        self._level = 0
        self._primaries = []
        self._group = VGroup()

        # fill-in level 0
        self._primaries.append(Circle(radius=self._radius, color=self._s_colour, fill_opacity=1.0).set_z_index(1))
        self._group.add(self._primaries[0])
        self.play(Create(self._primaries[0]))

    def nextLevel(self):
        self._level += 1

        if self._level > 1:
            # next level, reset the infected primary nodes to be the
            # secondary infections of the previous level
            self._primaries = []
            for primary in self._secondaries.keys():
                for i in self._infected[primary]:
                    self._primaries.append(self._secondaries[primary][i])
        self._secondaries = dict()
        self._edges = dict()
        self._infected = dict()

        # create the animations
        animations = []
        spacing = self._level_width / (self._fan - 1)
        for primary in self._primaries:
            c = primary.get_center() + (self._level_width / 2) * LEFT + self._level_spacing * DOWN
            z = primary.get_z_index()
            self._secondaries[primary] = []
            self._edges[primary] = []
            for i in range(self._fan):
                # create the secondary nodes
                s = Circle(radius=self._radius, color=self._s_colour, fill_opacity=1.0).move_to(c).set_z_index(z)
                e = Line(primary.get_center(), s.get_center()).set_z_index(z - 1)
                self._group.add(s, e)
                c += spacing * RIGHT

                # create animations to display these new nodes
                animations.extend([Create(s), Create(e)])

                # store the new secondaries and their connecting edges
                self._secondaries[primary].append(s)
                self._edges[primary].append(e)
        self.play(AnimationGroup(*animations))

    def infections(self):
        if self._level == 1:
            # for level 1, infect the seed node first
            self.play(self._primaries[0].animate.set_color(self._i_colour).set_fill(self._i_colour))
            self.wait(1)

        # create the animations
        animations = []
        for primary in self._primaries:
            secondaries = self._secondaries[primary]

            # choose R secondary nodes to be infected
            infected = list(numpy.random.choice(range(len(secondaries)), self._R, replace=False))
            infected.sort()      # left to right
            self._infected[primary] = infected
            for i in infected:
                # change the colour for each secondary infection
                animations.append(secondaries[i].animate.set_color(self._i_colour).set_fill(self._i_colour))
        self.play(AnimationGroup(*animations))

    def removeUninfected(self):
        # create the animations
        animations = []
        for primary in self._primaries:
            secondaries = self._secondaries[primary]
            edges = self._edges[primary]
            infected = self._infected[primary]
            uninfected = [i for i in range(len(secondaries)) if i not in infected]
            for i in uninfected:
                # fade-out each uninfected node and its connecting edge
                animations.extend([FadeOut(secondaries[i]), FadeOut(edges[i])])
                self._group.remove(secondaries[i], edges[i])
        self.play(AnimationGroup(*animations))

    def arrangeLevel(self):
        bottomWidth = self._level_width * (self._R ** (self._levels - 1)) + self._sibling_spacing * (self._R ** (self._levels - 1) - 1)
        spacing = bottomWidth / (self._R ** self._level + 1)

        # create the animations
        animations = []
        for primary in self._primaries:
            secondaries = self._secondaries[primary]
            edges = self._edges[primary]
            infected = self._infected[primary]
            c = primary.get_center() + (self._R - 1) * spacing / 2 * LEFT + self._level_spacing * DOWN
            for i in infected:
                # move noide and edge to new spacing
                animations.append(secondaries[i].animate.move_to(c))
                animations.append(edges[i].animate.put_start_and_end_on(primary.get_center(), c))
                c += spacing * RIGHT
        self.play(AnimationGroup(*animations))

    def shift(self):
        self.play(self._group.animate.shift(UP))

    def construct(self):
        R = 2
        fan = 3
        levels = 4

        self.begin(R, fan, levels)
        for level in range(1, levels):
            self.nextLevel()
            self.infections()
            self.removeUninfected()
            if level == 1:
                label = MathTex('\mathcal{R}_0').shift(2 * RIGHT + UP)
                arrow = Arrow(start=label.get_left(), end=ORIGIN + RIGHT + 0.5 * DOWN)
                self._group.add(label, arrow)
                self.play(FadeIn(label))
                self.play(Create(arrow))
            self.arrangeLevel()
            if level < levels - 1:
                self.shift()

        self.wait(5)
