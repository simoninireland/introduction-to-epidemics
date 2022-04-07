import numpy
from manim import *

from pathlib import Path
sourceDir = Path(__file__).resolve().parent
logoPath = sourceDir.joinpath('physical-distancing.png')


class Header(Scene):
    '''A scene showingf a common header for videos.'''

    def construct(self):
        logo = ImageMobject(logoPath)

        title = Text('Epidemic modelling', font='sans-serif', font_size=48, weight=BOLD)
        subtitle = Text('Some notes, maths, and code', font='sans-serif').next_to(title, DOWN).align_to(title, LEFT, alignment_vect=RIGHT)
        titlebox = VGroup(title, subtitle).shift(LEFT, 0.5 * UP)
        chaptertitle = Text('Epidemic thresholds', font='sans-serif', slant=ITALIC).next_to(titlebox, DOWN).align_to(title, LEFT, alignment_vect=RIGHT).shift(DOWN)

        self.play(FadeIn(logo))
        self.wait(1)
        self.play(logo.animate.shift(3 * LEFT))

        self.play(Write(titlebox))
        self.wait(1)
        self.play(Write(chaptertitle))

        self.wait(5)
