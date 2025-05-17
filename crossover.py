import numpy as np

class Crossover:
    @staticmethod
    def single_point(parents, offspring_size, ga_instance):
        """
        Implementacja krzyżowania jednopunktowego.
        """
        offspring = []
        idx = 0
        while len(offspring) != offspring_size[0]:
            parent1 = parents[idx % parents.shape[0], :].copy()
            parent2 = parents[(idx + 1) % parents.shape[0], :].copy()

            # Wybierz losowy punkt podziału
            random_split_point = np.random.choice(range(offspring_size[1]))

            # Stwórz potomka
            parent1[random_split_point:] = parent2[random_split_point:]
            offspring.append(parent1)

            idx += 1

        return np.array(offspring)

    @staticmethod
    def two_points(parents, offspring_size, ga_instance):
        """
        Implementacja krzyżowania dwupunktowego.
        """
        offspring = []
        idx = 0

        while len(offspring) != offspring_size[0]:
            parent1 = parents[idx % parents.shape[0], :].copy()
            parent2 = parents[(idx + 1) % parents.shape[0], :].copy()

            # Wybierz dwa losowe punkty podziału
            gene_length = offspring_size[1]
            point1, point2 = np.sort(np.random.choice(range(gene_length), size=2, replace=False))

            # Stwórz potomka
            temp = parent1[point1:point2].copy()
            parent1[point1:point2] = parent2[point1:point2]
            parent2[point1:point2] = temp

            offspring.append(parent1)

            idx += 1

        return np.array(offspring)

    @staticmethod
    def uniform(parents, offspring_size, ga_instance):
        """
        Implementacja krzyżowania jednorodnego.
        """
        offspring = []
        idx = 0

        while len(offspring) != offspring_size[0]:
            parent1 = parents[idx % parents.shape[0], :].copy()
            parent2 = parents[(idx + 1) % parents.shape[0], :].copy()

            # Dla każdego genu, losowo wybierz rodzica
            for gene_idx in range(offspring_size[1]):
                if np.random.random() < 0.5:
                    parent1[gene_idx] = parent2[gene_idx]

            offspring.append(parent1)

            idx += 1

        return np.array(offspring)