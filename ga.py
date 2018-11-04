import random
random.seed()



class geneticAlgorithm:
    def __init__(self, l, p, objective_function):
        self.of = objective_function
        self.total_fitness = 0
        self.l = l
        self.p = p
        self.population = []
        self.next_gen = []
        self.mutation_rate = 1000
        self.mutations = 0
        self.generation = 0

    def generatePopulation(self):
        self.generation = 0
        for _ in range(self.p):
            s = []
            for _ in range(self.l):
                s.append(str(random.randrange(0,2)))
            self.addString(s)

    def addString(self, string):
        c = child(string, self.of)
        self.population.append(c)
        self.total_fitness += c.value

    def reproduce(self):
        self.generation += 1
        self.next_gen = []
        for _ in range(self.p):
            parent = random.random() * self.total_fitness
            for seed in self.population:
                parent -= seed.value
                if parent < 0:
                    c = child(seed.string, self.of)
                    self.next_gen.append(c)
                    break
        self.population = self.next_gen
        self.next_gen = []
    
    def crossover(self):
        self.next_gen = []
        for _ in range(self.p // 2):
            a = self.population[random.randrange(0, len(self.population))]
            b = self.population[random.randrange(0, len(self.population))]
            k = random.randrange(1, self.l - 1)
            c1 = child(a[:k] + b[k - self.l:], self.of)
            c2 = child(b[:k] + a[k - self.l:], self.of)
            self.next_gen.append(c1)
            self.next_gen.append(c2)
        self.population = self.next_gen
        self.next_gen = []

    def mutate(self):
        mutations = self.l * self.p / self.mutation_rate
        if random.random() <= mutations % 1:
            mutations += 1
        mutations = int(mutations)
        for _ in range(mutations):
            s = random.randrange(0, self.p)
            c = random.randrange(0, self.l)
            self.population[s][c] = '1' if self.population[s][c] == '0' else '0'
            self.mutations += 1

    def updateFitness(self):
        self.total_fitness = 0
        for s in self.population:
            self.total_fitness += s.value

    def displayPopStats(self, show_ga_stats):
        print("Generation:", self.generation)
        if show_ga_stats:
            print("Population Size:", self.p)
            print("String Size:", self.l)
            print("Mutation Rate:", self.mutation_rate)
        print("Total Fitness:", self.total_fitness)
        print("Average Fitness:", self.total_fitness / self.p)
        print("################################################")
        

class child:
    def __init__(self, string, objective_function):
        self.string = string
        self.objective_function = objective_function
        self.value = self.objective_function(string)

    def updateString(self, string):
        self.string = string
        self.value = self.objective_function(string)

    def __str__(self):
        return "(" + ''.join(self.string) + ", " + str(self.value) + ")"
    __repr__ = __str__
    def __getitem__(self, item):
        return self.string[item]

    def __setitem__(self, item, value):
        self.string[item] = value
        self.value = self.objective_function(self.string)

def objective_function(s):
    count = 0
    for i, c in enumerate(s):
        if c == '1':
            count += 2 ** i
    return count

# Use string size divisible by 10
# Max value 
def dejong_of(s):
    fitness = 0
    for i, c in enumerate(s):
        if i % 10 == 0:
            if i != 0:
                cur /= 100
                fitness += cur * cur
            cur = -512
        if c == '1':
            cur += 2 ** (i % 10)
    cur /= 100
    fitness += cur * cur
    return fitness

def main():
    ga = geneticAlgorithm(30, 50, dejong_of)
    ga.generatePopulation()
    print(ga.total_fitness, ga.population)
    for _ in range(1000):
        ga.reproduce()
        ga.crossover()
        ga.mutate()
        ga.updateFitness()
        ga.displayPopStats(False)

main()