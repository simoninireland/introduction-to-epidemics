# Preface

We recently unexpectedly found ourselves in a situation in which the
science of diseases is of critical importance to us all. The covid-19
pandemic provided us with a dramatic example of what damage a new
pandemic disease can cause to human health and happiness. It would be
nice to think that this is the only pandemic we'll encounter in our
lifetimes, but unfortunately we can't have confidence in that, and we
need to prepare ourselves and our societies for future outbreaks.

On an individual level, we want to know what to expect of lockdowns,
vaccines or other therapies. At a population level, we want to know
how diseases become epidemics and then pandemics, and how different
countermeasure strategies might influence their course. Above all, we
want certainty that the disease will be conquered and the future will
be better.

Scientists don't really *do* certainty, though. All of science is
based around the *models* that we construct to tell us about the
things we're interested in, and the *experiments* that we conduct to
see whether the models match the reality on the ground. It's
this combination of model and experiment, trial and error and
correction, that help us understand the world.

But what *is* a model of a disease? How do they work, and what can
they tell us about what we can expect from epidemics and other events?
I wrote this book as an attempt to explain the one small corner of
this vast field that I know something about: how to model epidemics
using network science and computer simulations. It isn't in any way
comprehensive, leaving huge areas unexplored and a huge number of
questions unanswered. I make it available in the hope that it may be
useful, and may encourage you to take an interest in science.


## Preface to the 1.1 edition

After writing the first edition we realised that we had a lot of
awkwardness in the `epydemic` library we were using: things that had
made sense when we built it, but that were clearly making life
difficult when doing lots of real computations. As a result we
upgraded the library to simplify many operations, notably how to
capture the progress of simulations.

While the 1.1 edition adds little new content, it does reflect these
simplifications, as well as reflecting some changes to diagram
construction and to the build process in general.
