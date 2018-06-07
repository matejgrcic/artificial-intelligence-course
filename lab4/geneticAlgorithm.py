import numpy as np


class GeneticAlgorithm(object):
    """
        Implement a simple generationl genetic algorithm as described in the instructions
    """

    def __init__(self, chromosomeShape,
                 errorFunction,
                 elitism=1,
                 populationSize=25,
                 mutationProbability=.1,
                 mutationScale=.5,
                 numIterations=10000,
                 errorTreshold=1e-6
                 ):
        self.populationSize = populationSize  # size of the population of units
        self.p = mutationProbability  # probability of mutation
        self.numIter = numIterations  # maximum number of iterations
        self.e = errorTreshold  # threshold of error while iterating
        self.f = errorFunction  # the error function (reversely proportionl to fitness)
        self.keep = elitism  # number of units to keep for elitism
        self.k = mutationScale  # scale of the gaussian noise

        self.i = 0  # iteration counter
        # initialize the population randomly from a gaussian distribution
        # with noise 0.1 and then sort the values and store them internally

        self.population = []
        for _ in range(populationSize):
            chromosome = np.random.randn(chromosomeShape) * 0.1

            fitness = self.calculateFitness(chromosome)
            self.population.append((chromosome, fitness))

        # sort descending according to fitness (larger is better)
        self.population = sorted(self.population, key=lambda t: -t[1])

    def step(self):
        """
            Run one iteration of the genetic algorithm. In a single iteration,
            you should create a whole new population by first keeping the best
            units as defined by elitism, then iteratively select parents from
            the current population, apply crossover and then mutation.
            The step function should return, as a tuple:
            * boolean value indicating should the iteration stop (True if
                the learning process is finished, False othwerise)
            * an integer representing the current iteration of the
                algorithm
            * the weights of the best unit in the current iteration
        """

        self.i += 1

        #############################
        #       YOUR CODE HERE      #
        #############################
        new_population = self.bestN(self.keep)
        while len(new_population) < self.populationSize:
            parents = self.selectParents()
            child = self.crossover(*parents)
            child = self.mutate(child);
            fitness = self.calculateFitness(child)
            new_population.append((child, fitness))
        self.population = sorted(new_population, key=lambda t: -t[1])
        should_stop = self.i > self.numIter or self.best()[1] < self.e
        return should_stop, self.i, self.best()[0]

    def calculateFitness(self, chromosome):
        """
            Implement a fitness metric as a function of the error of
            a unit. Remember - fitness is larger as the unit is better!
        """
        chromosomeError = self.f(chromosome)

        #############################
        #       YOUR CODE HERE      #
        #############################
        return 1 / chromosomeError

    def bestN(self, n):
        """
            Return the best n units from the population
        """
        #############################
        #       YOUR CODE HERE      #
        #############################
        return self.population[0:n]

    def best(self):
        """
            Return the best unit from the population
        """
        #############################
        #       YOUR CODE HERE      #
        #############################
        return self.population[0]

    def selectParents(self):
        """
            Select two parents from the population with probability of
            selection proportional to the fitness of the units in the
            population
        """
        #############################
        #       YOUR CODE HERE      #
        #############################
        sum = 0
        for unit in self.population:
            sum += unit[1]

        parents = []
        threshold = np.random.uniform(0, sum)
        current = 0
        for unit in self.population:
            current += unit[1]
            if current > threshold:
                parents.append(unit)
                break

        threshold = np.random.uniform(0, sum)
        current = 0
        for unit in self.population:
            current += unit[1]
            if current > threshold:
                parents.append(unit)
                break

        return parents

    def crossover(self, p1, p2):
        """
            Given two parent units p1 and p2, do a simple crossover by
            averaging their values in order to create a new child unit
        """
        #############################
        #       YOUR CODE HERE      #
        #############################
        child = []
        for i in range(0, len(p1[0])):
            child.append((p1[0][i] + p2[0][i])/2.)
        return np.array(child)

    def mutate(self, chromosome):
        """
            Given a unit, mutate its values by applying gaussian noise
            according to the parameter k
        """

        #############################
        #       YOUR CODE HERE      #
        #############################
        for i in range(len(chromosome)):
            if np.random.random() < self.p:
                chromosome[i] += np.random.normal(0, self.k)
        return chromosome