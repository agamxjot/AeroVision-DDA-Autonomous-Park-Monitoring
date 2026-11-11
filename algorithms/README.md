# Algorithms

This directory contains the core algorithmic modules developed for the DDA Autonomous Park Monitoring System.

The modules support geographical inspection-point generation, graph optimization, drone-count calculation, route optimization, and simulation.

## Files and Modules

| File | Description |
|---|---|
| `Drone_Count_Algorithm.py` | Drone count calculation and related allocation logic |
| `HCP_Node_Generation.py` | Generates inspection nodes using Hexagonal Coverage Planning |
| `Kruskal_MST.py` | Implements Kruskal's Minimum Spanning Tree algorithm |
| `Simulation.py` | Simulation of the relevant planning or drone workflow |
| `TSP_Optimization.py` | Travelling Salesperson Problem-based route optimization |

## Algorithmic Workflow

The intended workflow connects geographical coverage generation with graph-based optimization and drone mission planning.

1. Generate inspection nodes from the park boundary.
2. Represent inspection locations as graph vertices.
3. Apply graph algorithms where required.
4. Optimize the waypoint visiting sequence.
5. Estimate drone requirements for inspection.
6. Evaluate the resulting workflow through simulation.

## Execution

Each Python script can be executed independently, subject to its configured input files and dependencies.

```bash
python HCP_Node_Generation.py
python Kruskal_MST.py
python TSP_Optimization.py
python Drone_Count_Algorithm.py
python Simulation.py
```

Check the input paths and parameters inside each script before execution.

## Notes

The exact inputs, outputs, and dependencies are defined by the individual implementations. Refer to the main project documentation for the overall architecture and methodology.