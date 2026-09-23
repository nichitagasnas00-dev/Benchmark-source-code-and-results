Algorithmic Performance Benchmarker

A Python-based benchmarking tool designed to measure, analyze, and visualize the empirical execution time and scaling behavior of fundamental algorithms against their theoretical Big-O time complexities.

Overview

Theoretical complexity analysis provides asymptotic bounds, but real-world execution depends on hardware architecture, cache locality, interpreter overhead, and input data distribution.This project benchmarks standard sorting and searching routines across scalable dataset sizes (from $10^2$ up to $10^6$ elements), evaluating how different memory layouts and initial element arrangements impact execution latency.

Features

Automated Complexity Profiling: Measures execution latency across user-defined dataset sizes ($N$).

Multi-Distribution Testing: Evaluates algorithms under multiple input conditions:
Randomly distributed uniform data (Average case)
Sorted data (Best / Worst case scenario depending on pivot selection
Reverse-sorted data (Degenerate case for naive partition algorithms)
High-duplicate arrays (Tests duplicate key efficiency)

High-Resolution Timing: Utilizes Python's time.perf_counter to ensure sub-millisecond precision.

Visual Performance Plots: Generates matplotlib graphs comparing empirical execution curves against theoretical $O(N \log N)$ and $O(N^2)$ growth curves.







