# Robust Distributed Estimation: Extending Gossip Algorithms to Ranking and Trimmed Means

This repository contains the official implementation of the experiments and figures in our paper, designed to make our research reproducible. 

## Repository Structure

```bash
├── configs/               # Configs used to run experiments
├── data/                  # LuftKlima Dataset and corresponding script
├── plot/                  # Utils to generate each figure
├── src/                   # Core source code (gossip algorithms)
├── README.md              # This file
├── requirements.txt       # Python dependencies
├── run_experiments.py     # Script to run experiments
└── run_figures.py         # Script to generate paper figures
```

## Getting Started

Install requirements using pip:
```bash
pip install -r requirements.txt
```
To run an experiment called "exp", you can simply use the following 
```bash
python run_experiments.py --exp_name "exp"
```

To generate a figure called "plot" from the paper, you can use the following
```bash
python run_figures.py --plot_name "plot"
```

## Experiments Compute Resources

The experiments are run on a single CPU with 32 GB of memory. The execution time for each experiment is given in the following table:

| Experiments | Execution Time | Figure
|-----------------|-----------------|----------
| exp1+exp2+exp3    | ~ 30 min     | Rank (a)
| exp4+exp5+exp6    | ~ 5 min     | Rank (b)
| exp7+exp8+exp9    | ~ 15 min     | Rank (c) 
| exp10+exp10a+exp10b    | ~ 50 min     | Trim (a) 
| exp11+exp12+exp13    | ~ 15 min     | Trim (b) 
| exp14    | ~ 5 min     | Trim (c)
| exp15+exp16+exp17    | ~ 5 min     | Rank (d)



## Basel Luftklima Dataset

The dataset contains temperature measurements from 99 Meteoblue sensors across the Basel region, recorded between April 14 and April 15, 2025. The dataset is available online at [https://data.opendatasoft.com/explore/dataset/100009\%40basel-stadt](https://data.opendatasoft.com/explore/dataset/100009\%40basel-stadt).
For each sensor, only the first observation is used. A graph is built by connecting sensors that are within 1 km of each other, based on their geographic coordinates. Only the connected component of the graph is kept. The corresponding script is in the data folder.
