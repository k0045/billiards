

import random


class Gene():
    def __init__(self):
        self.degree = 0 # 9bit
        self.speed  = 0 # 4bit
        self.score  = 0 

    def random_gene(self):
        self.degree = random.randint(0, 0b111111111)
        self.speed  = random.randint(0, 0b1111)
        return self

    @staticmethod
    def crossover(g1, g2):
        g = Gene()

        r = random.randint(0, 0b111111111)
        g.degree = (g1.degree & r) | (g2.degree & ~r)

        r = random.randint(0, 0b1111)
        g.speed = (g1.speed & r) | (g2.speed & ~r)

        return g

    def mutation(self):
        g = Gene()

        r = random.randint(0, 0b111111111)
        g.degree = (self.degree & r) | (0b111111111 & ~r)

        r = random.randint(0, 0b1111)
        g.speed = (self.speed & r) | (0b1111 & ~r)

        return g


class GA():
    GENES_NUM = 6
    def __init__(self):
        self.generation = 0 # generation number
        self.genes = [Gene()] * GA.GENES_NUM
        self.genesIter = 0


    def generate_next(self):
        if self.generation == 0:
            for i in range(GA.GENES_NUM):
                self.genes[i] = Gene().random_gene()
            return

        nextGenes = sorted(self.genes, key = lambda x: x.score, reverse = True)
        self.genes[0] = nextGenes[0]
        self.genes[1] = Gene.crossover(nextGenes[0], nextGenes[1])
        self.genes[2] = Gene.crossover(nextGenes[0], nextGenes[2])
        self.genes[3] = Gene.crossover(nextGenes[1], nextGenes[2])
        self.genes[4] = nextGenes[0].mutation();            
        self.genes[5] = nextGenes[0].mutation();            
        self.genes[6] = nextGenes[0].mutation();                    
        self.genes[7] = nextGenes[1].mutation();            
    
                



    def next(self):
        if self.genesIter >= GA.GENES_NUM:
            self.genesIter = 0
            self.generate_next()
            self.generation += 1
            print("%d generation" % self.generation)
            
        return self.genes[self.genesIter]


    def set_score(self, score):
        if self.generation == 0: # No genes are generated yet.
            return

        self.genes[self.genesIter - 1].score = score 