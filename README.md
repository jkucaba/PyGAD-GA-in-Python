# Genetic Algorithm Optimization Project

## Overview
This project implements a genetic algorithm (GA) to optimize mathematical functions using the PyGAD library. The program supports both binary and real-value representations, various selection, crossover, and mutation methods, and provides visualization of results.

## Features
- **Fitness Functions**: Includes the Martin-Gaddy function for optimization.
- **Binary and Real Representations**: Supports both binary and real-value encodings.
- **Selection Methods**: Tournament, roulette wheel (RWS), and random selection.
- **Crossover Methods**: Single-point, two-point, and uniform crossover.
- **Mutation Methods**: Random, swap, and Gaussian mutation.
- **Configuration Loader**: Load configurations from a JSON file.
- **Visualization**: Plots fitness history, solution trajectory, and 3D function surfaces.
- **Best Configuration Selector**: Automatically identifies and saves the best configuration.

## Project Structure

.
├── crossover.py # Crossover methods implementation
├── fitness_function.py # Fitness functions and binary decoding 
├── genetic_algorithm.py # Genetic algorithm setup and execution 
├── mutation.py # Mutation methods implementation 
├── config_loader.py # Configuration loader and best configuration selector 
├── visualizer.py # Visualization of results 
├── configs.json # JSON file with predefined configurations 
├── main.py # Main entry point for running experiments 
└── README.md # Project documentation

## Requirements
- Python 3.8+
- Libraries:
  - `pygad`
  - `numpy`
  - `matplotlib`


## Usage
1. Run the program:  
**python main.py**
2.  configurations in configs.json.
**If the file does not exist, a default configuration will be generated.**
3. Results:
**Logs and results are displayed in the console.**
**The best configuration is saved to best_config.json.**

## Example Configuration (configs.json)
```json
[
  {
    "name": "Real repr. + Tournament + Single-Point + Random",
    "num_generations": 50,
    "sol_per_pop": 50,
    "num_parents_mating": 25,
    "num_genes": 2,
    "init_range_low": -20,
    "init_range_high": 20,
    "gene_type": "float",
    "parent_selection_type": "tournament",
    "crossover_type": "single_point",
    "mutation_type": "random",
    "is_binary": false
  },
  {
    "name": "Binary repr. + RWS + Two-Points + Swap",
    "num_generations": 50,
    "sol_per_pop": 50,
    "num_parents_mating": 25,
    "num_genes": 2,
    "init_range_low": -20,
    "init_range_high": 20,
    "gene_type": "int",
    "parent_selection_type": "rws",
    "crossover_type": "two_points",
    "mutation_type": "swap",
    "bits_per_gene": 20,
    "is_binary": true
  }
]
```

## Output
Logs: Detailed logs of each configuration's performance.
Visualizations: Plots of fitness history, solution trajectory, and 3D function surface.
Best Configuration: Saved in best_config.json.

## Customization
Add new fitness functions in fitness_function.py.
Implement additional mutation or crossover methods in mutation.py or crossover.py.

## Example Code Snippets
**Fitness Function (fitness_function.py)**
```python
import numpy as np

class FitnessFunction:
    @staticmethod
    def martin_gaddy(x1, x2):
        term1 = (x1 - x2) ** 2
        term2 = ((x1 + x2 - 10) / 3) ** 2
        return term1 + term2
```

**Mutation Methods (mutation.py)**

```python
import numpy as np

class Mutation:
    @staticmethod
    def gaussian(offspring, ga_instance):
        for chromosome_idx in range(offspring.shape[0]):
            for gene_idx in range(offspring.shape[1]):
                if np.random.random() < 0.1:
                    offspring[chromosome_idx, gene_idx] += np.random.normal(0, 1)
        return offspring
```
**Genetic Algorithm Setup (genetic_algorithm.py)**

```python
import pygad

class GeneticAlgorithm:
    def __init__(self, config):
        self.config = config
        self.ga_instance = None

    def setup(self):
        self.ga_instance = pygad.GA(
            num_generations=self.config.num_generations,
            num_parents_mating=self.config.num_parents_mating,
            sol_per_pop=self.config.sol_per_pop,
            num_genes=self.config.num_genes,
            fitness_func=self.config.fitness_func
        )
```