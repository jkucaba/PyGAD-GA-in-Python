import os
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np

class Visualizer:
    @staticmethod
    def create_output_folder(config_name):
        """
        Create a folder structure for saving visualization outputs
        """
        safe_name = config_name.replace(' + ', '_').replace(' ', '_')

        results_dir = 'results'
        if not os.path.exists(results_dir):
            os.makedirs(results_dir)

        config_dir = os.path.join(results_dir, safe_name)
        if not os.path.exists(config_dir):
            os.makedirs(config_dir)

        return config_dir

    @staticmethod
    def plot_fitness_history(ga_instance, title_prefix=""):
        """
        Plots the fitness history throughout generations.
        """
        plt.figure(figsize=(10, 6))
        plt.plot(ga_instance.best_solutions_fitness, color='blue', linewidth=2)
        plt.title(f'{title_prefix}Fitness History')
        plt.xlabel('Generation')
        plt.ylabel('Fitness Value')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()

        output_dir = Visualizer.create_output_folder(title_prefix.strip(": "))
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f'fitness_history_{timestamp}.png'
        plt.savefig(os.path.join(output_dir, filename))
        plt.show()

    @staticmethod
    def plot_solution_trajectory(ga_instance, title_prefix=""):
        """
        Rysuje trajektorię najlepszych rozwiązań na płaszczyźnie funkcji celu.
        """
        plt.figure(figsize=(10, 8))

        solutions = np.array(ga_instance.best_solutions)

        if solutions.ndim == 1 or (solutions.ndim == 2 and solutions.shape[1] == 1):
            best_solution = ga_instance.best_solution()[0]
            solutions = np.array([best_solution])

        if hasattr(ga_instance, 'is_binary') and ga_instance.is_binary:
            from fitness_function import FitnessFunction
            decoded_solutions = []
            for solution in solutions:
                decoded = FitnessFunction.decode_binary(
                    solution,
                    ga_instance.gene_range_high,
                    ga_instance.gene_range_low,
                    ga_instance.num_genes_original,
                    ga_instance.bits_per_gene
                )
                decoded_solutions.append(decoded)
            solutions = np.array(decoded_solutions)

        x = np.linspace(-20, 20, 100)
        y = np.linspace(-20, 20, 100)
        X, Y = np.meshgrid(x, y)
        Z = (X - Y) ** 2 + ((X + Y - 10) / 3) ** 2

        contour = plt.contourf(X, Y, Z, levels=50, cmap='Blues')
        plt.colorbar(contour, label='Function Value')

        if len(solutions) > 1:
            plt.plot(solutions[:, 0], solutions[:, 1], '.-', color='royalblue',
                     markersize=8, linewidth=1.5, alpha=0.7, label='Search Trajectory')
        else:
            plt.plot(solutions[0][0], solutions[0][1], 'o', color='royalblue',
                     markersize=8, alpha=0.7, label='Best Solution')

        plt.scatter([5], [5], c='yellow', s=250, marker='*',
                    edgecolors='black', linewidth=1, label='Global Optimum [5,5]')

        plt.title(f'{title_prefix}Trajectory of Best Solutions')
        plt.xlabel('x₁')
        plt.ylabel('x₂')
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()

        output_dir = Visualizer.create_output_folder(title_prefix.strip(": "))
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f'solution_trajectory_{timestamp}.png'
        plt.savefig(os.path.join(output_dir, filename))
        plt.show()

    @staticmethod
    def plot_3d_function_surface(ga_instance, title_prefix=""):
        """
        Rysuje powierzchnię funkcji celu w 3D z trajektorią najlepszych rozwiązań.
        """
        fig = plt.figure(figsize=(14, 8))
        ax = fig.add_subplot(111, projection='3d')

        # Pobierz najlepsze rozwiązania z każdej generacji
        solutions = np.array(ga_instance.best_solutions)

        # Sprawdź wymiary tablicy rozwiązań i przekształć ją w razie potrzeby
        if solutions.ndim == 1 or (solutions.ndim == 2 and solutions.shape[1] == 1):
            best_solution = ga_instance.best_solution()[0]
            solutions = np.array([best_solution])

        if hasattr(ga_instance, 'is_binary') and ga_instance.is_binary:
            from fitness_function import FitnessFunction
            decoded_solutions = []
            for solution in solutions:
                decoded = FitnessFunction.decode_binary(
                    solution,
                    ga_instance.gene_range_high,
                    ga_instance.gene_range_low,
                    ga_instance.num_genes_original,
                    ga_instance.bits_per_gene
                )
                decoded_solutions.append(decoded)
            solutions = np.array(decoded_solutions)

        x = np.linspace(-20, 20, 50)
        y = np.linspace(-20, 20, 50)
        X, Y = np.meshgrid(x, y)
        Z = (X - Y) ** 2 + ((X + Y - 10) / 3) ** 2

        surf = ax.plot_surface(X, Y, Z, cmap='coolwarm', alpha=0.6)
        fig.colorbar(surf, shrink=0.5, aspect=5)

        def martin_gaddy(solution):
            x1, x2 = solution[0], solution[1]
            return (x1 - x2) ** 2 + ((x1 + x2 - 10) / 3) ** 2

        if len(solutions) > 1:
            ax.scatter(solutions[:, 0], solutions[:, 1],
                      [martin_gaddy(s) for s in solutions],
                      c='blue', s=30, depthshade=False, alpha=0.5,
                      label='Solutions Trajectory')
        else:
            ax.scatter(solutions[0][0], solutions[0][1],
                      martin_gaddy(solutions[0]),
                      c='blue', s=50, depthshade=False,
                      label='Best Solution')

        ax.scatter([5], [5], [0], c='yellow', s=200, marker='*',
                  edgecolors='black', label='Global Optimum [5,5,0]')

        ax.set_title(f'{title_prefix}Martin and Gaddy Function Surface with Optimization Trajectory')
        ax.set_xlabel('x₁')
        ax.set_ylabel('x₂')
        ax.set_zlabel('Function Value')
        ax.legend(bbox_to_anchor=(1.1, 1), loc='upper left')
        plt.tight_layout()

        output_dir = Visualizer.create_output_folder(title_prefix.strip(": "))
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f'3d_surface_{timestamp}.png'
        plt.savefig(os.path.join(output_dir, filename))
        plt.show()