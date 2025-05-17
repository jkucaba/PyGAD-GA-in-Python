import json
import os
from mutation import Mutation
from genetic_algorithm import GeneticAlgorithm
from genetic_algorithm_config import GeneticAlgorithmConfig
import logging


class ConfigLoader:
    """
    Klasa do wczytywania konfiguracji z pliku JSON
    """

    @staticmethod
    def load_configs(config_file):
        """
        Wczytuje konfiguracje z pliku JSON
        """
        if not os.path.exists(config_file):
            logging.error(f"Plik konfiguracyjny {config_file} nie istnieje!")
            return []

        try:
            with open(config_file, 'r') as f:
                configs_json = json.load(f)

            configurations = []
            for config_json in configs_json:
                # Konwersja gene_type z string na odpowiedni typ
                if 'gene_type' in config_json:
                    if config_json['gene_type'] == 'float':
                        config_json['gene_type'] = float
                    elif config_json['gene_type'] == 'int':
                        config_json['gene_type'] = int

                # Konwersja mutation_type z string na odpowiednią funkcję
                if 'mutation_type' in config_json:
                    if config_json['mutation_type'] == 'gaussian':
                        config_json['mutation_type'] = Mutation.gaussian
                    elif config_json['mutation_type'] == 'swap':
                        config_json['mutation_type'] = Mutation.swap
                    # inne typy mutacji pozostają jako string

                # Tworzenie obiektu konfiguracji
                config = GeneticAlgorithmConfig(**{k: v for k, v in config_json.items() if k != 'name'})

                configurations.append({
                    'name': config_json['name'],
                    'config': config
                })

            return configurations

        except Exception as e:
            logging.error(f"Błąd podczas wczytywania pliku konfiguracyjnego: {str(e)}")
            return []

    @staticmethod
    def save_default_config(filename='configs.json'):
        """
        Zapisuje domyślną konfigurację do pliku JSON
        """
        default_configs = [
            {
                'name': 'Real repr. + Tournament + Single-Point + Random',
                'num_generations': 50,
                'sol_per_pop': 50,
                'num_parents_mating': 25,
                'num_genes': 2,
                'init_range_low': -20,
                'init_range_high': 20,
                'gene_type': 'float',
                'parent_selection_type': 'tournament',
                'crossover_type': 'single_point',
                'mutation_type': 'random',
                'is_binary': False
            },
            {
                'name': 'Real repr. + RWS + Two-Points + Swap',
                'num_generations': 50,
                'sol_per_pop': 50,
                'num_parents_mating': 25,
                'num_genes': 2,
                'init_range_low': -20,
                'init_range_high': 20,
                'gene_type': 'float',
                'parent_selection_type': 'rws',
                'crossover_type': 'two_points',
                'mutation_type': 'swap',
                'is_binary': False
            },
            {
                'name': 'Real repr. + Random + Uniform + Gaussian',
                'num_generations': 50,
                'sol_per_pop': 50,
                'num_parents_mating': 25,
                'num_genes': 2,
                'init_range_low': -20,
                'init_range_high': 20,
                'gene_type': 'float',
                'parent_selection_type': 'random',
                'crossover_type': 'uniform',
                'mutation_type': 'gaussian',
                'is_binary': False
            },
            {
                'name': 'Binary repr. + Tournament + Single-Point + Random',
                'num_generations': 50,
                'sol_per_pop': 50,
                'num_parents_mating': 25,
                'num_genes': 2,
                'init_range_low': -20,
                'init_range_high': 20,
                'gene_type': 'int',
                'parent_selection_type': 'tournament',
                'crossover_type': 'single_point',
                'mutation_type': 'random',
                'bits_per_gene': 20,
                'is_binary': True
            },
            {
                'name': 'Binary repr. + RWS + Two-Points + Swap',
                'num_generations': 50,
                'sol_per_pop': 50,
                'num_parents_mating': 25,
                'num_genes': 2,
                'init_range_low': -20,
                'init_range_high': 20,
                'gene_type': 'int',
                'parent_selection_type': 'rws',
                'crossover_type': 'two_points',
                'mutation_type': 'swap',
                'bits_per_gene': 20,
                'is_binary': True
            },
            {
                'name': 'Binary repr. + Random + Uniform + Gaussian',
                'num_generations': 50,
                'sol_per_pop': 50,
                'num_parents_mating': 25,
                'num_genes': 2,
                'init_range_low': -20,
                'init_range_high': 20,
                'gene_type': 'int',
                'parent_selection_type': 'random',
                'crossover_type': 'uniform',
                'mutation_type': 'gaussian',
                'bits_per_gene': 20,
                'is_binary': True
            }
        ]

        try:
            with open(filename, 'w') as f:
                json.dump(default_configs, f, indent=2)
            logging.info(f"Domyślna konfiguracja zapisana do pliku {filename}")
        except Exception as e:
            logging.error(f"Błąd podczas zapisywania domyślnej konfiguracji: {str(e)}")


class BestConfigSelector:
    """
    Klasa do wybierania najlepszej konfiguracji na podstawie wyników
    """

    @staticmethod
    def select_best_config(results):
        """
        Wybiera najlepszą konfigurację na podstawie wartości funkcji celu
        """
        best_name = None
        best_value = float('inf')

        for name, stats in results.items():
            if stats['function_value'] < best_value:
                best_value = stats['function_value']
                best_name = name

        return best_name, results[best_name] if best_name else None

    @staticmethod
    def save_best_config(best_name, best_stats, filename='best_config.json'):
        """
        Zapisuje najlepszą konfigurację do pliku JSON
        """
        best_config = {
            'name': best_name,
            'function_value': float(best_stats['function_value']),
            'generations': int(best_stats['generations']),
            'crossover_type': best_stats['crossover_type'],
            'mutation_type': str(best_stats['mutation_type']),
            'parent_selection_type': best_stats['parent_selection_type']
        }

        if 'decoded_solution' in best_stats:
            best_config['solution'] = best_stats['decoded_solution'].tolist()
        else:
            best_config['solution'] = best_stats['best_solution'].tolist()

        try:
            with open(filename, 'w') as f:
                json.dump(best_config, f, indent=2)
            logging.info(f"Najlepsza konfiguracja zapisana do pliku {filename}")
        except Exception as e:
            logging.error(f"Błąd podczas zapisywania najlepszej konfiguracji: {str(e)}")


class Main:
    @staticmethod
    def run(config_file='configs.json'):
        # Inicjalizacja logowania
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        logger = logging.getLogger('GA_Logger')

        # Sprawdzenie czy plik konfiguracyjny istnieje, jeśli nie to utworzenie go
        if not os.path.exists(config_file):
            logger.info(f"Plik konfiguracyjny {config_file} nie istnieje. Tworzenie domyślnej konfiguracji...")
            ConfigLoader.save_default_config(config_file)

        # Wczytanie konfiguracji z pliku
        configurations = ConfigLoader.load_configs(config_file)

        if not configurations:
            logger.error("Nie udało się wczytać konfiguracji. Używanie konfiguracji domyślnych...")
            # Tutaj można dodać domyślne konfiguracje jak w pierwotnym kodzie
            # lub wyjść z programu
            return

        results = {}

        # Testy
        for config_data in configurations:
            logger.info(f"\n\n=== Testing configuration: {config_data['name']} ===")
            ga = GeneticAlgorithm(config_data['config'])
            ga.setup()
            stats = ga.run()
            results[config_data['name']] = stats

        logger.info("\n\n=== Comparison of all configurations ===")
        for name, stats in results.items():
            if 'decoded_solution' in stats:
                solution_str = f"Decoded: {stats['decoded_solution']}"
            else:
                solution_str = f"Solution: {stats['best_solution']}"

            logger.info(f"Configuration: {name}")
            logger.info(f"{solution_str}")
            logger.info(f"Function value: {stats['function_value']}")
            logger.info(f"Generations: {stats['generations']}")
            logger.info("---")

        # Wybór najlepszej konfiguracji
        best_name, best_stats = BestConfigSelector.select_best_config(results)

        if best_name:
            logger.info("\n\n=== Best configuration ===")
            logger.info(f"Configuration: {best_name}")

            if 'decoded_solution' in best_stats:
                logger.info(f"Decoded solution: {best_stats['decoded_solution']}")
            else:
                logger.info(f"Solution: {best_stats['best_solution']}")

            logger.info(f"Function value: {best_stats['function_value']}")
            logger.info(f"Generations: {best_stats['generations']}")

            # Zapisanie najlepszej konfiguracji do pliku
            BestConfigSelector.save_best_config(best_name, best_stats)

        return results


if __name__ == "__main__":
    Main.run()