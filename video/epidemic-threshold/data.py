from datetime import timedelta
import numpy
from epydemic import SIR, ERNetwork, StochasticDynamics
from epyc import ParallelLab, HDF5LabNotebook, Experiment
import matplotlib
matplotlib.rcParams['figure.dpi'] = 300
import matplotlib.pyplot as plt


# Compute time taken to create result set
def creationTime(nb):
    df = nb.dataframe()
    start = min(df[Experiment.START_TIME])
    end = max(df[Experiment.END_TIME])
    return end - start


# Create the default plot
def plotThreshold(nb, title, fn):
    fig = plt.figure(figsize=(5, 5))
    ax = plt.gca()

    df = nb.dataframe()
    pInfects = df[SIR.P_INFECT]
    rFraction = df[SIR.REMOVED] / df[ERNetwork.N]

    ax.scatter(pInfects, rFraction,
               s=0.1, c='red')
    ax.set_xlim([min(pInfects), max(pInfects)])
    ax.set_xlabel('$p_{infect}$')
    ax.set_ylabel('$R$')
    ax.set_ylim([0.0, 1.0])
    ax.set_title(title)

    plt.savefig(fn)


# Lab for the experiments
nb = HDF5LabNotebook('src/datasets/epidemic-threshold.h5')
lab = ParallelLab(nb, cores=-2)


# Define the experiment
def threshold_ER(pInfects):

    def run(lab):
        tag = lab.notebook().currentTag()
        print(f'Creating result set {tag}')

        lab[ERNetwork.N] = 10000
        lab[ERNetwork.KMEAN] = 40
        lab[SIR.P_INFECTED] = 0.001
        lab[SIR.P_REMOVE] = 0.002
        lab[SIR.P_INFECT] = pInfects
        lab['repetitions'] = range(50)

        m = SIR()
        e = StochasticDynamics(m, ERNetwork())
        lab.runExperiment(e)

        print('Created result set "{tag}" in {d:.02f}s'.format(tag=tag,
                                                               d=creationTime(nb).seconds))

    return run


# Perform the experiment
lab.createWith('er-network', description='Epidemic threshold on an ER network',
               f=threshold_ER(numpy.linspace(0.0, 1.0, num=50)),
               finish=True)
plotThreshold(nb, 'Epidemic threshold on an ER network', 'video/epidemic-threshold/er-threshold.png')


# Narrow the experiment to the region around the threshold
lab.createWith('er-network-focus', description='Epidemic threshold on an ER network, focusing on the threshold region',
               f=threshold_ER(numpy.linspace(0.00001, 0.0002, num=50)),
               finish=True)
plotThreshold(nb, 'Epidemic threshold on an ER network (focused)', 'video/epidemic-threshold/er-threshold-focused.png')
