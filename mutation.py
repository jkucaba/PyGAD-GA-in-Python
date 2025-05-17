import numpy as np
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('GA_Logger')


class Mutation:
    @staticmethod
    def gaussian(offspring, ga_instance):
        """
        Implementacja mutacji Gaussa.
        """
        for chromosome_idx in range(offspring.shape[0]):
            for gene_idx in range(offspring.shape[1]):
                if np.random.random() < 0.1:
                    # Dodaj losowe zaburzenie z rozkładu normalnego
                    offspring[chromosome_idx, gene_idx] += np.random.normal(0, 1)

        return offspring

    @staticmethod
    def adaptive_gaussian(offspring, ga_instance):
        """
        Implementacja adaptacyjnej mutacji Gaussa (skala maleje z czasem).
        """
        generation = ga_instance.generations_completed
        max_gen = ga_instance.num_generations
        scale = max(0.1, 1 - generation / max_gen)

        for chromosome_idx in range(offspring.shape[0]):
            for gene_idx in range(offspring.shape[1]):
                if np.random.random() < 0.2:
                    offspring[chromosome_idx, gene_idx] += np.random.normal(0, scale)

        return offspring

    @staticmethod
    def swap(offspring, ga_instance):
        """
        Implementacja mutacji przez zamianę indeksów.
        """
        for chromosome_idx in range(offspring.shape[0]):
            if np.random.random() < 0.1:
                # Wybieramy dwa losowe punkty
                gene_indices = np.random.choice(range(offspring.shape[1]), size=2, replace=False)

                # Zamieniamy wartości
                temp = offspring[chromosome_idx, gene_indices[0]]
                offspring[chromosome_idx, gene_indices[0]] = offspring[chromosome_idx, gene_indices[1]]
                offspring[chromosome_idx, gene_indices[1]] = temp

        return offspring


def on_generation(ga_instance):
    """
    Callback function called after each generation.
    """
    if ga_instance.generations_completed % 10 == 0:
        logger = logging.getLogger('GA_Logger')
        best_solution = ga_instance.best_solution()[0]
        best_fitness = ga_instance.best_solution()[1]

        if hasattr(ga_instance, 'is_binary') and ga_instance.is_binary:
            from fitness_function import FitnessFunction
            decoded = FitnessFunction.decode_binary(
                best_solution,
                ga_instance.gene_range_high,
                ga_instance.gene_range_low,
                ga_instance.num_genes_original,
                ga_instance.bits_per_gene
            )
            function_value = 1.0 / best_fitness - 1e-10

            logger.info(f"Generation = {ga_instance.generations_completed}")
            logger.info(f"Decoded solution = {decoded}")
            logger.info(f"Function value = {function_value}")
        else:
            function_value = 1.0 / best_fitness - 1e-10

            logger.info(f"Generation = {ga_instance.generations_completed}")
            logger.info(f"Best solution = {best_solution}")
            logger.info(f"Function value = {function_value}")