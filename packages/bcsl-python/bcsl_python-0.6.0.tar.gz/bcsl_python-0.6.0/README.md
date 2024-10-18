# BCSL Python

Python port of the Bootstrap-based Causal Structure Learning Algorithm. Depends on the causal-learn package for scoring.


## Installation

```bash
pip install bcsl-python causal-learn
```

## Usage

```python
import numpy as np

from bcsl import BCSL

# Generate synthetic data for testing
n_samples = 200

# Independent variables
Var1 = np.random.normal(0, 1, n_samples)
Var2 = np.random.normal(0, 1, n_samples)

# Dependent variables
Var3 = 2 * Var1 + np.random.normal(0, 1, n_samples)  # Var3 depends on Var1
Var4 = 0.5 * Var2 + np.random.normal(0, 1, n_samples)  # Var4 depends on Var2
Var5 = (
        Var3 + Var4 + np.random.normal(0, 1, n_samples)
)  # Var5 depends on Var3 and Var4
data = pd.DataFrame(
    {"Var1": Var1, "Var2": Var2, "Var3": Var3, "Var4": Var4, "Var5": Var5}
)
bcsl = BCSL(data, num_bootstrap_samples=4)

# Step 1: Learn local skeletons using HITON-PC
local_skeletons = bcsl.learn_local_skeleton()
print("Local Skeletons:", local_skeletons)

# Step 2: Resolve asymmetric edges using bootstrap
undirected_graph = bcsl.combine_local_to_global_skeleton()
print("Global Skeleton (resolved):", bcsl.global_skeleton)
print("Undirected Graph:", undirected_graph)

# Step 3: Orient edges using BDeu and hill-climbing
dag = bcsl.orient_edges()
print("Final DAG:", dag)
```

## Reference
Xianjie Guo, Yujie Wang, Xiaoling Huang, Shuai Yang, and Kui Yu. 2022. Bootstrap-based Causal Structure Learning. In Proceedings of the 31st ACM International Conference on Information & Knowledge Management (CIKM '22). Association for Computing Machinery, New York, NY, USA, 656–665. https://doi.org/10.1145/3511808.3557249