The progession of a disease
===========================

Everyone suffers from a disease at some point. The lucky amongst us
avoid anything more serious that influenza, measles, or (in my case,
long ago) whooping cough. But all diseases share some comon
characteristics: characteristics so common, in fact, that their
mathematical properties are shared by other processes that aren't
actually diseases at all, including the spread of computer viruses
{cite}`KW91` and the spread of rumours or other information.

The diseases in which we are interested are caused by *pathogens*,
typically viruses or bacteria: simple living organisms that make their
home in humans (or other living organisms) and cause some adverse
reaction as a result of their lifecycle. These pathogens can pass
between individuals in a number of ways, causing the disease to
spread. A disease might be airborne, able to live in the air and be
breathed by passing individuals. It might be deposited on objects and
picked up by future physical contact with the contaminated
surfaces. Or it might be communicable only by direct contact, skin to
skin, through sex, or might require an even closer contact such as a
blood transfusion. It might be foodborne, transmitted through
contaminated food that infects several people from a common source. It
might be vectored through an animal, as is the case for malaria. And
finally there is a class of non-communicable diseases such as cancer
or heart disease, typically not caused directly by pathogens but
perhaps influenced by their presence.

Each different kind of disease will have its own characteristic
pathology when it infects a person, and also its own epidemiology that
controls how it spreads. Clinically, both these characteristics are
extremely important. From a network science perspective we focus on
the epidemiology, but the pathology remains important, because factors
involved in how a disease progresses *in* individuals may have a
profound effect on how it spreads *between* individuals.


## Disease progression

A person's infection goes through several periods. Once infected, the
disease resides **latent** in their system, not showing symptoms and
not being infectious to others. After this latent period the disease
becomes infectious, capable of being spread to others: this is the
**infectious** period. Typically a person's infectiousness peaks and
dies away before the end of the disease progression.

![Disease stages](disease-periods.png)

These two periods &ndash; latent and infectious &ndash; control the
*transmission* of infection. After initial infection, however, there
is an **incubation** period before the person shows symptoms of the
disease. After the onset of symptoms, the disease progresses and ends
in some **resolution**: the patient gets better, or dies. If they
recover, they may then have some immunity to further infection.

![Disease types](disease-types.png)

For different diseases, the lengths of these periods and the ways they
overlap vary. For **Type A** diseases, the incubation period is longer
than the latent period. This means that a patient can start to
transmit the disease before the disease becomes manifest in
themselves. This happens in cases of measles. In **Type B** diseases
such as SARS or ebola, by contrast, the incubation period is shorter
than the latent period, meaning that asymptomatic patients cannot
infect others. So despite ebola being a more feared disease than
measles, it may be easier to treat epidemiologically since
quarantining patients showing symptoms will prevent transmission in
the general population (although not to medical staff); in measles,
transmission starts before symptoms show themselves, so quarantine
based on symptoms is less effective. Moreover for some disease the
infectious period may continue after the patient has died: the corpses
of victims of ebola, which are transmitted *via* bodily fluids, can be
extremely infectious for some time after death, meaning that funerals
become very dangerous loci of potential infection for mourners.

How long do the different periods last? For each disease there will be
typical durations, often with substantial variance. In the case of
ebola, for example, a typical timeline would be a 0&ndash;3 day
incubation period, a 7&ndash;12 day progression to recovery or death,
and a latent period of 2&ndash;5 days. The ranges give the variance of
periods, different for different individuals that depend on factors
including the severity of infection and the individual's overall
health. However, the incubation period for ebola can be up to 21 days,
meaning that a suspected case needs to be quarantined for this period:
long enough, in other words, for the disease symptoms to manifest if
the person is actually infected. While one can test for most diseases
(including ebola) in a laboratory, during an epidemic such tests may
overwhelm the public health infrastructure, making quarantine the most
practical option. (During historical disease outbreaks, of course,
quarantine was the *only* option.)


Measuring and modelling epidemics
---------------------------------

Epidemiology is the science of creating models of diseases and their
spread that can be analysed, to make predictions or to simulate the
effects of different responses. To do this, we need to identify the
core elements of a disease from the perspective of transmission: we do
not need to understand the disease's biology, only the timings and
other factors that affect its spread.

We discussed above the periods of diseases, their relationships, and
their different, often characteristics, periods and variances. We need
some other numbers as well, however, and it turns out that these can
be measured directly in the field.

The first important number is known as the **secondary attack rate**,
denoted 2&deg;AR. This measures what proportion of people exposed to
each for each primary case will develop infection. For example in the
first ebola outbreak 498 family members were exposed to infected
relatives, of whom 38 developed ebola themselves. This gives a
2&deg;AR of $38 / 498 = 7.6\%$.

There are a couple of caveats with this number. Firstly, 2&deg;AR only
applies to small populations, typically villages: it doesn't scale-up
to whole populations. Secondly, 2&deg;AR is very context-sensitive and
depends on the degree of contact that individuals have with the
infected individual: for close family members, the 2&deg;AR in the
first ebola outbreak was around 27% rather than around 8%. Thirdly,
individuals may become increasingly infectious as their own infection
progresses. Fourthly, disease organisms are subject to natural
selection and, since they reproduce quickly, can vary in their
infectiousness over time. The selection pressures often lead to
diseases become progressively more transmissible but less severe,
eventually become sufficiently weak for people's immune systems to be
able to cope with them directly &ndash; and the epidemic dies out.

The second important metric is the **basic case reproduction number**,
denoted $R_0$. $R_0$ represents the total number of secondary
infections expected for each primary infection in a totally
susceptible population. The $0$ in $R_0$ stands for $t = 0$: the basic
case reproduction number applies at the start of an epidemic. Over
time, the number of people susceptible to infection will vary as they
become infected, recover, die, and so forth. We can account for this
by developing a **net case reproduction number** $R_t$ by multiplying
$R_0$ by the susceptible fraction of the population at time $t$.

$R_0$ is affected by three factors:

1. The duration of infectiousness. All other things being equal, a
disease with a longer period of infectiousness has more time in which
to infect other patients.
2. The probability of transmission at each contact. Some diseases are
extremely contagious, with each contact having a high probability of
passing on the infection; others are much harder to pass one to
secondary cases.
3. The rate of contact. Someone coming into contact with a lot of
susceptible individuals will have more opportunities to generate a
secondary case than someone meeting fewer people.

The first two factors are characteristic of the disease, derived from
its biology. The third is affected by the social conditions in which
the epidemic takes place: it is this factor that quarantine affects,
by reducing (to zero) the contacts an infected person has with
uninfected individuals.

These two metrics, 2&deg;AR and $R_0$, are related. If we compute
2&deg;AR for the different circumstances of contact &ndash; family,
neighbours, community, and so forth &ndash; and multiply each by the
number of contacts a person has in each circumstance, we can sum them
to get $R_0$:

\begin{align}
    R_0 &= 2^oAR_{family} \times contacts_{family} \\
        &+ 2^oAR_{neighbours} \times contacts_{neighbours} \\
        &+ 2^oAR_{community} \times contacts_{community} \\
        &+ \cdots
\end{align}

As with disease periods, $R_0$ is an average that is affected by
various factors and is best treated as a mean value with some
variance: some infected individuals will affect more people, some
less, but *on average* they will generate $R_0$ secondary infections.


Controlling epidemics
---------------------

The importance of $R_0$ is that it indicates whether, and how fast, a
disease can spread through a susceptible population. If $R_0 < 1$ then
we expect fewer than one secondary case per primary. This means that
each "generation" of the disese will be smaller than the one that
infected it, and the disease will die out. If $R_0 = 1$ then the
disease will perpetuate itself in whatever size of population was
originally infected. Nature is never so precise as to present us with
a disease like this, of course. However, $R_0 = 1$ is the *threshold
value* about which diseases become epidemics. If $R_0 > 1$, the
disease will break-out and infect more and more people exponentially
quickly. Exactly *how* quickly depends on how large $R_0$ is. For
measles, $R_0 \ge 15$ &ndash; fifteen new infections for each case
&ndash; which explains how measles spread so quickly in unvaccinated
populations. Different strains of influenza have different ranges of
$R_0$: for the[1918 "Spanish flu"
epidemic](https://en.wikipedia.org/wiki/1918_flu_pandemic) it has been
estimated {cite}`VTM07` that $1.2 \le R_0 \le 3.0$ in the community
(although substantially more in confined settings). If this sounds
benign, remember that this epidemic killed more people than the First
World War. Perhaps interesting in light of its media coverage, for
ebola we have $1.5 \le R_0 \le 2.7$ {cite}`Alt14`, roughly the same as
a not-too-severe winter flu outbreak.

In order to bring an epidemic under control, then, we need to reduce
the *effective* value of $R_0$. This will generally happen anyway
through mutation and selection as the disease agent (typically a
bacterium or a virus) evolves. We can quarantine infected individuals
so that they do not cause further secondary infections. This is
clearly more effective with Type B diseases than with Type A, since
the latter will have already become infectious before they become
symptomatic.

A more effective approach is to reduce the susceptible fraction of the
population. The approach is to make the value of $R_t$ less than one
(the epidemic threshold) so that the disease dies out naturally. This
happens naturally in diseases to which individuals have natural or
acquired immunity, for example by surviving a bout of the disease.

An even more effective approach is to artificially give people
immunity: vaccination. A vaccine, where it exists, confers full or
partial immunity on its recipients.

