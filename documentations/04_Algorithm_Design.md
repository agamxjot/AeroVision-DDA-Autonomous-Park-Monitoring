# 4. Algorithm Design

## 4.1 Introduction

The project integrates multiple algorithmic techniques to support geographical coverage, route optimization, and multi-drone coordination.

## 4.2 Hexagonal Coverage Planning

The HCP approach distributes inspection points across a geographical region using a hexagonal arrangement.

The method uses the drone's calculated ground coverage radius to determine the spacing between neighboring inspection points.

Its purpose is to provide systematic inspection-point distribution across the park.

## 4.3 Graph Representation

The generated inspection points can be represented as vertices in a graph.

Edges represent possible connections between inspection points, with their weights corresponding to geographical distances.

This representation allows graph-based algorithms to be applied to the inspection network.

## 4.4 Kruskal's Minimum Spanning Tree

Kruskal's algorithm is used in the graph-processing workflow to construct a Minimum Spanning Tree (MST).

The algorithm:
1. Sorts graph edges in ascending order of weight.
2. Selects the shortest available edge.
3. Checks whether adding the edge creates a cycle.
4. Adds the edge if it does not create a cycle.
5. Continues until the required spanning structure is formed.

The resulting MST connects the graph vertices while minimizing the total selected edge weight.

## 4.5 Travelling Salesperson Problem (TSP)

The TSP formulation is used to determine an efficient visiting order for inspection waypoints.

The objective is to minimize the total route distance while visiting the required inspection points.

## 4.6 Nearest Neighbour Initialization

The nearest-neighbour heuristic is used to construct an initial route.

Starting from an initial waypoint, the algorithm repeatedly selects the nearest unvisited waypoint until all required points have been visited.

This provides an initial route that can subsequently be improved.

## 4.7 2-Opt Optimization

The 2-opt algorithm improves the initial route by examining pairs of route edges.

If replacing two edges with an alternative connection reduces the total route distance, the route is updated.

This process is repeated until no further improvement is found under the implemented search procedure.

## 4.8 Algorithm Integration

The overall algorithmic workflow is:

HCP Node Generation → Graph Construction → Graph Optimization → Initial Route Generation → 2-Opt Improvement → Optimized Waypoint Sequence.

The optimized waypoint sequence is then passed to the drone mission-planning module.

**Implementation note:** Document Kruskal as part of the implemented system only if the corresponding code in the ALGORITHMS directory actually performs the MST calculation. An MST alone does not guarantee a shortest closed TSP tour.