import random
random.seed()
nov = 0
noterms = 0
Lines = []


class geneticAlgorithm:
    def __init__(self, l, p, objective_function, looking_for):
        self.of = objective_function
        self.total_fitness = 0
        self.l = l #length of genome
        self.p = p # size of the population
        self.population = []
        self.next_gen = []
        self.mutation_rate = 1000
        self.mutations = 0
        self.generation = 0
        self.fitness_history = 0 #switch to check if min/max value was updated: 0 - no change; 1 - changed
        self.looking_for_maximum = looking_for  #True - looking for global max, False - global min
        self.x = None   #initial x of max/min f(x). currently is the string value. needs to be changed to dec before displaying
        self.y = None   #initial f(x) which is a local max/min. 
        self.elite = None #string of best result of cur gen. Added to next gen

    def generatePopulation(self):
        self.generation = 0
        for i in range(self.p):
            s = []
            for _ in range(self.l):
                s.append(str(random.randrange(0,2)))
            self.addString(s)
            self.updateXY(self.population[i])
        self.elite = self.x     

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
        # Next lines take out last mutated string and put best result of previous generation instead.
        c = self.population.pop() ##
        self.population.append(child(self.elite, self.of)) ##
     

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
        local_x = self.population[0].string
        local_y = self.population[0].value
        for s in self.population:
            self.total_fitness += s.value
            self.updateXY(s)
            ## Searches for "elite" of current population 
            if (self.looking_for_maximum and s.value > local_y):
                local_x = s.string
                local_y = s.value
            elif (not self.looking_for_maximum and s.value < local_y):
                local_x = s.string
                local_y = s.value
        self.elite = local_x
			
    def displayPopStats(self, show_ga_stats):
        print("Generation:", self.generation)
        if show_ga_stats:
            print("Population Size:", self.p)
            print("String Size:", self.l)
            print("Mutation Rate:", self.mutation_rate)
        print("Total Fitness:", self.total_fitness)
        print("Average Fitness:", self.total_fitness / self.p)
        print("################################################")
        
    # updates current min/max x and f(x)  
    def updateXY(self, s): 
        if (self.x == None or self.y == None):
            self.x = s.string
            self.y = s.value
            self.fitness_history = 1
        else:
            if (self.looking_for_maximum  and s.value > self.y):
                self.y = s.value
                self.x = s.string
                self.fitness_history = 1
            elif (not self.looking_for_maximum and s.value < self.y):
                self.y = s.value
                self.x = s.string
                self.fitness_history = 1
    
    #returns current min/max x and f(x)  
    #TODO convert x from string
    def getResult(self):
        return self.x, self.y
    
    def resetFitness(self):
        self.fitness_history = 0
        
    #returns True if stalled
    def checkStall(self):
        if (self.fitness_history == 0):
            #print("stalled")
            return True
        else:
            return False
	
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

def dynamic_of(s):
    a = [0]
    for char in s:
        if "0" in char:
            a.append(-1)
        else:
            a.append(int(char)) 
    return eval(Lines[1])

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

def useWhich():
    of = (0,0,None,True)
    userRequest = input("Use which Objective Function? (dejong: d, from file: f): ")
    if "d" in userRequest:
        of = (30,50,dejong_of,False)
    elif "f" in userRequest:
        userRequest = input("How many values? (10 - 27): ")
        line = (int(userRequest) - 10) * 2
        print(line)
        file = open("given_of.txt", "r")
        file.seek(0)
        i = 0
        while i < line:
            file.readline()
            i+=1
        Lines.append(file.readline())
        Lines.append(file.readline()[:-2])
        of = (int(userRequest), 50, dynamic_of, False)
    return of

def main():
    iterations = []
    max_y = 0
    max_x = 0
    stall_check_frequency = 100
    generations_limit = 5000
    looking_for_max = True # maximizing function for this test
    of = useWhich()
    print(of)
    for _ in range(10):
        ga = geneticAlgorithm(*of)
        ga.generatePopulation()
        ga.displayPopStats(True)
        iterations_counter = 0
        stall = False
        while (iterations_counter < generations_limit and not stall):
            ga.reproduce()
            ga.crossover()
            ga.mutate()
            ga.updateFitness()
            #ga.displayPopStats(False)
            if ((iterations_counter+1) % stall_check_frequency == 0):
                stall = ga.checkStall()
                ga.resetFitness()    
      
            iterations_counter += 1
            ga.displayPopStats(True)
            
        x, y = ga.getResult()
        print("Result {} corresponds to {}".format(y, x))
        print("Did ",iterations_counter, " iterations")
        iterations.append(y)
        if y >max_y and of[3]:
            max_x = x
            max_y = y
        elif y < max_y and not of[3]:
            max_x = x
            max_y = y
    print(iterations)
    print("Top result: ")
    print (max_y, max_x)
    
main()
