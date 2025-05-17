class GeneticAlgorithmConfig:
    def __init__(self,
                 num_generations=100,
                 sol_per_pop=50,
                 num_parents_mating=25,
                 num_genes=2,
                 init_range_low=0,
                 init_range_high=2,
                 gene_type=int,
                 parent_selection_type="tournament",
                 crossover_type="single_point",
                 mutation_type="random",
                 K_tournament=3,
                 bits_per_gene=20,
                 is_binary=False):
        self.num_generations = num_generations
        self.sol_per_pop = sol_per_pop
        self.num_parents_mating = num_parents_mating
        self.num_genes = num_genes
        self.init_range_low = init_range_low
        self.init_range_high = init_range_high
        self.gene_type = gene_type
        self.parent_selection_type = parent_selection_type
        self.crossover_type = crossover_type
        self.mutation_type = mutation_type
        self.K_tournament = K_tournament
        self.bits_per_gene = bits_per_gene
        self.is_binary = is_binary