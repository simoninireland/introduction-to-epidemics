# Models and modelling

We should first clarify what is means to model something, or to
develop a model: what models are, what we expect from them, their
advantages and limitations.


## Models

By **{index}`model`** we mean a formal description of some aspects of
a system of interest that we can explore in order to gain insight into
the behaviour of the real system.

A **{index}`mathematical model <model;mathematical>`** consists of
one or more equations expressing the relationships between different
quantities. There are often some **parameters** involved, quantities
whose values are known or assumed.

```{margin}
One can also have **mechanical** models, of course, such as the orreries
that model the motions of planets. In some senses machines are just
computation models that happen to use analogue components rather than
digital.
```
A **{index}`computational model <model;computational>`**, by contrast, is a program written to simulate the
behaviour of the system. Such simulations are almost always based on
underlying mathematical models and include parameters. What do
computers provide? Sets of equations can often be understood (or
"solved analytically") by purely symbolic means, but many systems of
equations *can't* be solved this way and instead need to be solved
numerically, by starting with specific values (numbers) and showing
how they evolve under the equations. Even for equations that *can* be
solved analytically, computers are often useful tools for helping to
explore large systems, or for visualising the results.


## Uses of models

There are lots of questions we might want to ask about systems, and
these can often give rise to different models drawing on different
styles and approaches to modelling. For definiteness, let's
discuss some of the questions we might ask about epidemics.

We might be interested in **epidemics in general**. How do changes in
infectiousness affect the spread of the disease? What are the
relationships between infectiousness and recovery? How do different
patterns of contacts in a population affect how it spreads? What are
the effects of different countermeasures, like physical distancing,
vaccination, or quarantine? Are there any patterns in the epidemic,
like multiple waves? These are quite abstract questions that could be
asked of *any* disease, and answering them might tell us something
about how *all* diseases behave -- including those we encountered yet.

On the other hand, we might be interested in **a specific disease**, or
even in **a specific outbreak**. How will *this* disease spread in a
population? How about in another country to the one it's currently in?
How will a *particular* countermeasure affect the spread? When will it
be safe for the majority of people to return to work? These are all
very concrete questions that depend on the exact details of the
situation about which they're asked, and answering them may be
massively useful in managing this situation. (Taylor provides an
accessible discussion of the uses and interpretations of the well-known
Imperial College model of {index}`covid-19`'s impact on UK NHS bed availability
during the 2020 outbreak {cite}`Tay20`.)

```{margin}
There's a saying among doctors who deal with outbreaks on the
ground: "When you've seen one pandemic, you've ... seen one pandemic."
The lessons learned often don't translate to new situations.
```
The interplay between these two kinds of questions is quite
complicated. In concrete cases we presumably measure the specifics of
the outbreak and work with them. We only have partial control, for
example on enforcing social distancing. It's often hard to then make
more general predictions about diseases more widely, to draw
conclusions that can be used in other cases.

So should we be more abstract? Abstraction typically brings control
over the model: we can explore a whole range of modes of transmission,
for example rather than just the one we happen to have for this
disease. We can explore different countermeasures in the model without
committing to one, which means there are no consequences for being
wrong. We get to observe some general patterns and draw general
conclusions &ndash; which then don't *exactly* apply to *any* real
disease.

On the other hand, the conclusions we draw from these abstract models
can't be applied blindly to particular situations on the ground. A
good example (which we'll come to {doc}`later <thresholds>`) concerns
the conditions under which an epidemic can get established in a
population. One would want to be *very* careful in taking the results
of an abstract investigation of this phenomenon and then concluding
that an epidemic can't occur in a specific population &ndash; very
careful that the model's assumptions were respected, very careful that
the parameters were known, and so forth. Mistakes in situations like
this can mean that outbreaks get out of control, and people may die.


## Assumptions

The accuracy of a model depends on its **{index}`assumptions <model;assumptions>`**,
and how well these match reality. This issue appears
in several guises. The model's "mechanics" &ndash; the ways it fits
its various elements together &ndash; need to match the disease it's
(purporting to be) a model of. It needs to identify the parameters
that control its evolution.  These parameters need to match those of
the real disease.

All these are problematic at the best of times, but especially when
dealing with a new disease that's not been well-studied. How
infectious is a disease? How long is a person sick for? Does the
disease confer immunity on an individual who's had it? &ndash; and is
that immunity total or partial, permanent or time-limited?  All these
factors introduce uncertainties into any conclusions we draw from
modelling.


## Correctness

Whether we're interested in concrete or abstract questions, we still
have the problem of **{index}`correctness`**: does our model produce the
"right" answers? It might not, either because it has been built
incorrectly (has "bugs" in computer terms &ndash; but mathematical
equations have them too), or because we don't know the values of some
of the parameters (especially problematic in the middle of an
outbreak, when measurement often takes a back seat to treatment), or
because there are aspects of the real world that we haven't considered
but that affect the result (often the case for more abstract models).

We know quite a lot about building software, much of which applies to
the building of computer models: unit {index}`testing`, integration testing,
clear documentation, source {index}`version control`, and so on. With modelling
we then face the additional problem of deciding whether the code we've
built is fit for purpose. 

```{margin}
Computer scientists often split the question of assuring
correctness into two parts: **verification** ("did we build the thing
right?") and **validation** ("did we build the right thing?").
```
Deciding what "fit" means is an interesting question in its own
right. It's something we may only know retrospectively: did the
results that came out of the model match what happened on the ground?
We may not be able to measure exactly what *did* happen on the ground:
did we count all the fatalities, or were some missed, or
mis-diagnosed? For a more abstract model, how happy are we that our
simplifications don't entirely divorce us from reality?

## Stochastic processes

There's another problem.

Suppose you have the misfortune of becoming ill. For a fortnight you
are infectious, and there's a chance that you'll infect anyone you
meet. Now we know that you don't infect *everyone* &ndash; no disease
(fortunately) is so contagious &ndash; so you infect a fraction of all
those you *could* have infected. We can't usually predict this
exactly, but the exact details may matter: rather than infect Aunt
Carol, who's a noted recluse who has no further opportunities to
infect anyone else, you instead happen to infect Cousin Charlotte
who's a noted party animal and goes on to spread the illness
widely. So even if we know the general pattern of a disease, the exact
way in spreads is affected by chance factors.

A system like this is referred to as a **{index}`stochastic process`**. They
include an element of randomness in their very nature: it's *not* a
bug, it's a feature.

```{margin}
One way to think about what's happening is that each run of the model
is sampling the distribution of possible outcomes. You expect to
seldom see "unlikely" outcomes and mainly see "likely" ones &ndash;
but sometimes you'll see an "unlikely" outcome by chance.
```
Now consider what this means for modelling. We can take exactly the
same situation &ndash; the same disease, the same population &ndash;
run the model twice, get two different answers &ndash; and them *both*
be right! The way to think about this is that each run is a "possible
outcome" of the disease. There may be several possible outcomes, and
they may all be similar &ndash; or there may be radical
differences. (We'll see an example of this in a later chapter.)

We often think that every problem has a "right" answer, but for
stochastic processes this isn't the case: there are many "right"
answers. It's attractive to think that we can simply "debug" our way
out of trouble, but in fact we can't. There may be randomness we can't
engineer away.

What to do? Actually, computer science is unusual in "normally" having
single answers. If you ask a biologist how long butterflies live for,
you don't expect her to go out and observed the lifespan of
*every single butterfly* before answering. Instead you get a
statistical answer: an average and some variance. It's the same for
stochastic models: we run the model several times (possibly hundreds
of times) for the same inputs and collate the results. 

```{margin}
At least in principle. It can be tricky to accomplish in practice, not
least because computer scientists have expended a lot of ingenuity in
making their pseudo-random number sequences less pseudo and more
random.
```
In a computer model, it's often possible to actually reproduce exactly
even a stochastic process, because the "{index}`random numbers`" we use are
actually only pseudo-random and so can be re-created. That can help in
the narrow sense of seeing whether the model produces the same results
given the same inputs *and* the same "random" numbers, but it doesn't
help in the wider sense of capturing the behaviour of a system with
*inherent* randomness.


(sec:model-expectations)=
## Managing our expectations

```{margin}

This is captured by the classic aphorism,
[attributed](https://en.wikipedia.org/wiki/All_models_are_wrong) to the
statistician George Box, that "all models are wrong, but some are
useful ... the approximate nature of the model must always be
borne in mind".
```
This all sounds like modelling is a horrible mess. But the situation
isn't hopeless. 

We need to be careful. The results we get from any model, of any kind,
are tentative and suggestive and can generate insight into the system
the model is seeking to represent, whether concretely or
abstractly. There will always be factors outwith the model's
consideration. The results aren't "true" in any exact sense. They need
to be interpreted by people who understand both
the phenomena *and* models *and* modelling. This will often lead to
the realisation that the model needs to be changed, or extended or
enriched, and sometimes even simplified and stripped-down, better to
answer the questions that are being posed.

When we quipped in the preface that "scientists don't really do
certainty", it's this that we had in mind.

```{epigraph}
Science is sometimes criticised for pretending to explain everything,
for thinking that it has an answer to every question. It's a curious
accusation. As every researcher working in every laboratory throughout
the world knows, doing science means coming up hard against the limits
of your ignorance on a daily basis -- the innumerable things that you
don't know and can't do. This is quite different from claiming to know
everything. ... But if we are certain of nothing, how can we possibly
rely on what science tells us? The answer is simple. Science is not
reliable because it provides certainty. It is reliable because it
provides us with the best answers we have at present. Science is the
most we know so far about the problems confronting us. It is precisely
its openness, the fact that it constantly calls current knowledge into
question, which guarantees that the answers it offers are the best so
far available: if you find better answers, those new answers become
science. ... The answers given by science are not reliable because they are
definitive. They are reliable because they are not definitive. They
are reliable because they are the best answers available today. And
they are the best we have because we don't consider them to be
definitive, but see them as open to improvement. It's the awareness of
our ignorance that gives science its reliability.

-- Carlo Rovelli {cite}`Rov17`.
```

Modelling, like experimentation, is both integral to science and
subject to it: both a tool and an object of study, to be approached
sceptically and refined through time. The study of epidemics is an
excellent example of this process, and we can progressively refine our
models better to reflect our improving understanding.


## Questions for discussion

- What can models tell us about real-world disease epidemics?

- Suppose you were asked to advise political leaders on the basis of
  what a model predicts. Would you? What would you want them to know
  about the process of modelling?

