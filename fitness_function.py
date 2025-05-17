import numpy as np

class FitnessFunction:
    @staticmethod
    def martin_gaddy(x1, x2):
        """
        Funkcja Martina i Gaddy: f(x1,x2) = (x1-x2)^2 + ((x1+x2-10)/3)^2
        Minimum globalne: f(5,5) = 0
        """
        term1 = (x1 - x2) ** 2
        term2 = ((x1 + x2 - 10) / 3) ** 2
        return term1 + term2

    @staticmethod
    def fitness_func_real(ga_instance, solution, solution_idx):
        """
        Funkcja dopasowania dla reprezentacji rzeczywistej.
        """
        x1, x2 = solution[0], solution[1]
        result = FitnessFunction.martin_gaddy(x1, x2)

        return 1.0 / (result + 1e-10)

    @staticmethod
    def fitness_func_binary(ga_instance, solution, solution_idx):
        """
        Funkcja dopasowania dla reprezentacji binarnej.
        """
        bits_per_gene = ga_instance.bits_per_gene
        gene_range_low = ga_instance.gene_range_low
        gene_range_high = ga_instance.gene_range_high
        num_genes = ga_instance.num_genes_original

        # Dekodowanie
        decoded = FitnessFunction.decode_binary(
            solution,
            gene_range_high,
            gene_range_low,
            num_genes,
            bits_per_gene
        )

        x1, x2 = decoded[0], decoded[1]
        result = FitnessFunction.martin_gaddy(x1, x2)

        # Minimalizacja, więc zwracamy odwrotność
        return 1.0 / (result + 1e-10)

    @staticmethod
    def decode_binary(binary_solution, max_val, min_val, num_genes, bits_per_gene):
        """
        Dekoduje reprezentację binarną do wartości rzeczywistych
        """
        decoded_solution = np.zeros(num_genes)
        for i in range(num_genes):
            # Pobranie bitów
            start_idx = i * bits_per_gene
            end_idx = start_idx + bits_per_gene
            gene_bits = binary_solution[start_idx:end_idx]

            # Konwersja
            decimal_value = 0
            for bit_idx, bit in enumerate(gene_bits):
                decimal_value += bit * (2 ** (bits_per_gene - bit_idx - 1))

            # Mapowanie na zakres
            max_decimal = 2 ** bits_per_gene - 1
            gene_value = min_val + ((max_val - min_val) * decimal_value) / max_decimal
            decoded_solution[i] = gene_value

        return decoded_solution