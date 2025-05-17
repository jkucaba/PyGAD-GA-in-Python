import pygad
from visualizer import Visualizer
from fitness_function import FitnessFunction
import logging
from mutation import on_generation

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('GA_Logger')


class GeneticAlgorithm:
    def __init__(self, config):
        self.config = config
        self.ga_instance = None
        self.result_stats = {}

        # Dodaj atrybuty potrzebne dla reprezentacji binarnej
        if config.is_binary:
            self.bits_per_gene = config.bits_per_gene
            self.gene_space = [[0, 1]] * (config.num_genes * config.bits_per_gene)
            self.num_genes_actual = config.num_genes * config.bits_per_gene
        else:
            self.gene_space = [{'low': config.init_range_low, 'high': config.init_range_high}] * config.num_genes
            self.num_genes_actual = config.num_genes

    def setup(self):
        # Dla reprezentacji binarnej
        if self.config.is_binary:
            self.is_binary = True
            self.bits_per_gene = self.config.bits_per_gene
            self.gene_range_low = self.config.init_range_low
            self.gene_range_high = self.config.init_range_high
            self.num_genes_original = self.config.num_genes

            self.ga_instance = pygad.GA(
                num_generations=self.config.num_generations,
                num_parents_mating=self.config.num_parents_mating,
                sol_per_pop=self.config.sol_per_pop,
                num_genes=self.config.num_genes * self.config.bits_per_gene,
                init_range_low=0,
                init_range_high=2,
                gene_type=int,
                parent_selection_type=self.config.parent_selection_type,
                crossover_type=self.config.crossover_type,
                mutation_type=self.config.mutation_type,
                mutation_percent_genes=10,
                keep_elitism=5,
                on_generation=on_generation,
                gene_space=[0, 1],
                fitness_func=FitnessFunction.fitness_func_binary
            )

            self.ga_instance.is_binary = self.is_binary
            self.ga_instance.bits_per_gene = self.bits_per_gene
            self.ga_instance.gene_range_low = self.gene_range_low
            self.ga_instance.gene_range_high = self.gene_range_high
            self.ga_instance.num_genes_original = self.num_genes_original
        else:
            # Dla reprezentacji rzeczywistej
            self.ga_instance = pygad.GA(
                num_generations=self.config.num_generations,
                num_parents_mating=self.config.num_parents_mating,
                sol_per_pop=self.config.sol_per_pop,
                num_genes=self.config.num_genes,
                init_range_low=self.config.init_range_low,
                init_range_high=self.config.init_range_high,
                gene_type=self.config.gene_type,
                parent_selection_type=self.config.parent_selection_type,
                crossover_type=self.config.crossover_type,
                mutation_type=self.config.mutation_type,
                mutation_percent_genes=10,
                keep_elitism=5,
                on_generation=on_generation,
                fitness_func=FitnessFunction.fitness_func_real
            )
            self.is_binary = False

    def run(self):
        """
        Uruchamia algorytm genetyczny i wizualizuje wyniki.
        """
        self.ga_instance.run()

        # Najlepsze rozwiązanie
        solution, solution_fitness, solution_idx = self.ga_instance.best_solution()
        actual_fitness = 1.0 / solution_fitness

        self.result_stats = {
            "best_solution": solution,
            "function_value": actual_fitness,
            "generations": self.ga_instance.generations_completed,
            "crossover_type": self.config.crossover_type,
            "mutation_type": self.config.mutation_type,
            "parent_selection_type": self.config.parent_selection_type
        }

        if self.config.is_binary:
            decoded_solution = FitnessFunction.decode_binary(
                solution,
                self.config.init_range_high,
                self.config.init_range_low,
                self.config.num_genes,
                self.config.bits_per_gene
            )
            self.result_stats["decoded_solution"] = decoded_solution

            logger.info("\n=== Results ===")
            logger.info(f"Best solution (binary): {solution}")
            logger.info(f"Decoded solution: {decoded_solution}")
            logger.info(f"Function value: {actual_fitness}")
            logger.info(f"Number of generations: {self.ga_instance.generations_completed}")
            logger.info(f"Global optimum should be at [5.0, 5.0] with value 0.0")
        else:
            logger.info("\n=== Results ===")
            logger.info(f"Best solution: {solution}")
            logger.info(f"Function value: {actual_fitness}")
            logger.info(f"Number of generations: {self.ga_instance.generations_completed}")
            logger.info(f"Global optimum should be at [5.0, 5.0] with value 0.0")

        title_prefix = "Binary Representation: " if self.config.is_binary else "Real Representation: "

        Visualizer.plot_fitness_history(self.ga_instance, title_prefix)
        Visualizer.plot_solution_trajectory(self.ga_instance, title_prefix)
        Visualizer.plot_3d_function_surface(self.ga_instance, title_prefix)

        return self.result_stats