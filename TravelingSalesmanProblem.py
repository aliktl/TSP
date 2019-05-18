from GeneticAlgorithmProblem import *
import random
import math
import time
import csv

class TravelingSalesmanProblem(GeneticAlgorithmProblem):
    
    genes = []
    dicLocations = {}
    gui = ''
    best = ''
    time = 0
    
    def __init__(self, data_mode,csvfile,numCities, height, width, time):
        print("Start of _init_ of TSP1")
        self.time = time
        if data_mode == 'Random':
            for itr in range(numCities):
                x = random.uniform(0, width)
                y = random.uniform(0, height)
                coordinate = [x, y]
                self.dicLocations[itr] = coordinate
        elif data_mode == 'Load':
            with open(csvfile, 'r') as my_csv:
                contents = list(csv.reader(my_csv, delimiter=","))
                for itr in range(len(contents)):
                    x, y = contents[itr][0],contents[itr][1]
                    self.dicLocations[itr] = [float(x),float(y)]
                    # print("self.dicLocations[itr]:", itr)
                    # print(type(self.dicLocations))

                    # print(self.dicLocations[itr])
        print(self.dicLocations)

    def registerGUI(self, gui):
        self.gui = gui

    def performEvolution(self, numIterations, numOffsprings, numPopulation, mutationFactor):
        print("Start of perform evolution")
        if self.gui != '':
            self.gui.start()

        startTime = time.time()
        # Here we create our initial population
        # print("Please understand the createInitialPopulation start")
        population = self.createInitialPopulation(numPopulation, len(self.dicLocations.keys()))
        # print("Please understand the createInitialPopulation end")
        while True:
            # print("start of while true of perform evolution")
            currentTime = time.time()
            if (currentTime - startTime) >= self.time:
                break
            offsprings = {}
            for itr in range(numOffsprings):
                # print("Start of for itr in range of perform evolution Offspring №:",int(itr))
                # Put a correct method name and an argument
                # HInt: You need a parent to create an offspring

                p1, p2 = self.selectParents(population)
                # print("p1, p2 = self.selectParents(population)")
                # After selecting a parent pair, you need to create
                # an offspring. How to do that?
                # Hint: You need to exchange the genotypes from parents
                offsprings[itr] = self.crossoverParents(p1,p2)
                # print("offsprings[itr] = self.crossoverParents(p1,p2)")
                factor = int(mutationFactor * len(self.dicLocations.keys()))
                # You need to add a little bit of changes in the
                # genotype to see a potential random evolution
                # this does not need information from either population
                # or parent
                self.mutation(offsprings[itr], factor)
                # print("self.mutation(offsprings[itr], factor)")
                # After creating an offspring set, what do you have to
                # perform?
                # HINT: You need to put the offspring in the population

            #print(population)
            population = self.substitutePopulation(population, offsprings)
            # print("population = self.substitutePopulation(population, offsprings)")

            # which method do you need to use the best solution? and
            # from where?
            mostFittest = self.findBestSolution(population)
            # print("mostFittest = self.findBestSolution(population)")
            self.best = mostFittest
            #print(self.best)
            # print("self.best = mostFittest")
            print(self.calculateTotalDistance(self.best))
            print(self.best.getGenotype())
            # print("print(self.calculateTotalDistance(self.best))")
            if self.gui != '':
                self.gui.update()

        endTime = time.time()
        # print("endTime = time.time()", endTime)
        # print("End of perform evolution")
        # print("return self.best.getGenotype(), self.fitness(self.best), self.calculateTotalDistance(self.best), (endTime - startTime)")
        return self.best.getGenotype(), self.fitness(self.best), self.calculateTotalDistance(self.best), (endTime - startTime)

    # genotype 하나가 주어졌을 때, Travel 거리를 계산하고, Utility(클수록 좋음) 계산하여 리턴
    def fitness(self, instance):
        # print("start of fitness")

        utility = 10000.0 / self.calculateTotalDistance(instance)

        return utility
    
    def calculateTotalDistance(self, instance):
        # This genotype is created based upon a position based encoding
        # Fill in the following blanks to complete this method
        # print("start of calculate total distance")
        genotype = instance.getGenotype()
        distance = 0.0
        #print(genotype)
        for itr in range(len(genotype)):
            current = self.dicLocations[genotype[itr]]

            next = self.dicLocations[genotype[itr + 1 if (itr + 1) != len(genotype) else 0]]
            #print(current, next)
            distance += self.calculateDistance(current, next)

            # print(distance)
        return distance
    
    def calculateDistance(self, coordinate1, coordinate2):
        # how to calculate the distance between two cities?
        # how to calculate the squre and the square root?
        # print("start of calculate distance")
        distance = math.sqrt((coordinate1[0]-coordinate2[0])**2 + (coordinate1[1]-coordinate2[1])**2)
        return distance

    def getPotentialGenes(self):
        # print("start of get potencial genes")
        return self.dicLocations.keys()

    def createInitialPopulation(self, numPopulation, numCities):
        # print("    def createInitialPopulation(self, numPopulation, numCities):")
        population = []
        # print("population = []")
              # print("for itr in range(numPopulation):", itr)
        for itr in range(numPopulation):
            genotype = list(range(numCities))
            # print("genotype = list(range(numCities))", genotype )

            random.shuffle(genotype)
                # print("random.shuffle(genotype)")
            instance = GeneticAlgorithmInstance()
            # print("instance = GeneticAlgorithmInstance()")
            instance.setGenotype(genotype)
            # print("instance.setGenotype(genotype)")
            population.append( instance )
            # print("population.append( instance ) ")
        # print("return population",)
        return population

        
    def isInfeasible(self, genotype):
        # print("start of isInfeasible")
        currentCity = 0
        visitedCity = {}
        for itr in range(len(genotype)):
            visitedCity[currentCity] = 1
            currentCity = genotype[currentCity]
            
        if len(visitedCity.keys()) == len(genotype): 
            return True
        else:
            return False
        
    def findBestSolution(self, population):
        # print("start of find best solution")
        idxMaximum = -1
        max = -99999
        for itr in range(len(population)):
            # print("start of for itr in range of findbestsolution №:", int(itr))
            if max < self.fitness(population[itr]):
                max = self.fitness(population[itr])
                idxMaximum = itr
        return population[idxMaximum]
    
    def selectParents(self, population):
        # print("def selectParents(self, population):")
        rankFitness = {}
        originalFitness = {}
        maxUtility = -999999
        minUtility = 999999

        #Max Util 과 Min Util 가지는 genotype 두 개 골라놓기
        for itr in range(len(population)):
            originalFitness[itr] = self.fitness(population[itr])
            if maxUtility < originalFitness[itr]:
                maxUtility = originalFitness[itr]
            if minUtility > originalFitness[itr]:
                minUtility = originalFitness[itr]

        # Population 을 utility가 높은 순부터 낮은 순으로 재배열
        for itr1 in range(len(population)):
            for itr2 in range(itr1+1, len(population)):
                if originalFitness[itr1] < originalFitness[itr2]:
                    originalFitness[itr1], originalFitness[itr2] = originalFitness[itr2], originalFitness[itr1]
                    population[itr1], population[itr2] = population[itr2], population[itr1]

        size = float(len(population))
        total = 0.0
        for itr in range(len(population)):
            rankFitness[itr] = (maxUtility + (float(itr) - 1.0)*(maxUtility - minUtility)) / (size - 1)
            total = total + rankFitness[itr]
        
        idx1 = -1
        idx2 = -1
        while idx1 == idx2:
            dart = random.uniform(0, total)
            sum = 0.0
            for itr in range(len(population)):
                sum = sum + rankFitness[itr]
                if dart <= sum:
                    idx1 = itr
                    break
            dart = random.uniform(0, total)
            sum = 0.0
            for itr in range(len(population)):
                sum = sum + rankFitness[itr]
                if dart <= sum:
                    idx2 = itr
                    break
        return population[idx1], population[idx2]
            
    def crossoverParents(self, instance1, instance2):
        # print("start of crossover parents")
        # G(a) chromosome
        genotype1 = instance1.getGenotype()
        # G(b) chromosome
        genotype2 = instance2.getGenotype()
        # G chromosome offspring
        newInstance = GeneticAlgorithmInstance()

        n = len(genotype1)
        fa = fb = True
        t = random.randint(0, n-1)
        x = genotype1.index(t)
        y = genotype2.index(t)
        g = [t]

        while fa or fb:
            x = (x-1) % n
            y = (y+1) % n
            if fa:
                if genotype1[x] not in g:
                    g.insert(0, genotype1[x])
                else:
                    fa = False

            if fb:

                if genotype2[y] not in g:
                    g.append(genotype2[y])
                else:
                    fb = False

        if len(g) < len(genotype1):
            left = [x for x in genotype1 if x not in g]
            random.shuffle(left)
            g.extend(left)

        #print(g)
        newInstance.setGenotype(g)
        
        return newInstance       
    
    def getMinimumNeighborNotVisitedCity(self, lstVisitedCity, dicNeighbor):
        # print("start of getMinimumNeighborNotVisitedCity")
        cities = list(dicNeighbor.keys())
        for itr in range(len(lstVisitedCity)):
            cities.remove(lstVisitedCity[itr])
        minimum = 999
        candidates = []
        for itr in range(len(cities)):
            location = cities[itr]
            if len(dicNeighbor[location]) <= minimum:
                minimum = len(dicNeighbor[location])
                candidates.append(location)
        random.shuffle(candidates)
        if len(candidates) == 0:
            return -1
        return candidates[0]
        
    def getNeighborCity(self, instance, currentCity):
        # print("start of getNeighborCity")
        genotype = instance.getGenotype()
        ret1 = -1
        ret2 = -1
        for itr in range(len(genotype)):
            if genotype[itr] == currentCity:
                ret1 = itr
                break
        ret2 = genotype[currentCity]
        neighbor = [ret1, ret2]
        return neighbor
    
    def mutation(self, instance, factor):
        # print("start of mutation")
        genotype = instance.getGenotype()


        for itr in range(factor):
            dist = self.calculateTotalDistance(instance)
            for _ in range(factor):
                idxSwap1 = random.randint(0, len(genotype) - 1)
                idxSwap2 = random.randint(0, len(genotype) - 1)
                if idxSwap1 > idxSwap2:
                    idxSwap1, idxSwap2 = idxSwap2, idxSwap1
                new_genotype = genotype[:]
                new_genotype[idxSwap1:idxSwap2+1] = genotype[idxSwap1:idxSwap2+1][::-1]

                instance.setGenotype(new_genotype)

                if self.calculateTotalDistance(instance) < dist:
                    genotype = new_genotype
                    break
                else:
                    instance.setGenotype(genotype)

        instance.setGenotype(genotype)
         
    def substitutePopulation(self, population, children):
        # print("start of substitutePopulation")
        for itr1 in range(len(population)):
            # print("start of for itr1 in range of substitutePopulation", int(itr1))
            for itr2 in range(itr1+1, len(population)):
                if self.fitness(population[itr1]) < self.fitness(population[itr2]):
                    population[itr1], population[itr2] = population[itr2], population[itr1]
        for itr in range(len(children)):
            population[len(population)-len(children)+itr] = children[itr]
        return population
