# Cabbage Merchant MDP

A Markov Decision Process (MDP) approach to the "Cabbage Merchant Problem," where we manage daily orders and uncertain shipments of cabbages with a 15% cancellation probability.

## Directory Structure

```
.
├── results
│   ├── policy.npy
│   └── value_function.npy
├── src
│   ├── simulation.py
│   └── value_iteration.py
├── readme.md
└── requirements.txt
```

### Files and Directories

* **results/** - Contains the converged optimal policy and value function files
  * `policy.npy` - Stores the optimal policy
  * `value_function.npy` - Stores the value function

* **src/** - Contains the source code
  * `value_iteration.py` - Implements the MDP model and runs value iteration
  * `simulation.py` - Simulates business operations using the optimal policy

## Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/ChengHua926/Sparc-2025-Write-Up.git cabbage-merchant-mdp
   cd cabbage-merchant-mdp
   ```

2. **Create and Activate a Virtual Environment (Optional)**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On Unix or MacOS:
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Running Value Iteration

Navigate to the `src/` directory and run:

```bash
python value_iteration.py
```

This runs a value iteration algorithm that may take up to an hour (depending on chosen parameters) to produce two files in `results/`:
* `policy.npy`
* `value_function.npy`

### Running Simulation

After generating the policy, you can simulate day-by-day performance:

```bash
python simulation.py
```

The simulation will:
* Load `policy.npy` from the `results/` folder
* Step through the MDP for a specified number of days
* Print total and average daily profit

## MDP Model Overview

### State Space
The state is represented as (O₁,O₂,O₃, A₁,A₂, c₁,c₂) where:
* O_i: Number of orders to fulfill in i days
* A_j: Number of cabbages arriving in j days
* c_j: Cancellation flags (0 or 1) for the corresponding shipments

### Action Space
Each day, you can:
* Accept (1) or reject (0) the incoming daily order
* Buy 0-5 cabbages for delivery in 2 days

### Transition Dynamics
* If c₁=0, the day's shipment arrives; otherwise no arrivals
* Deliver cabbages to meet O₁
* Shift O₁←O₂, O₂←O₃, etc.
* Draw a new cancellation flag for day-after-tomorrow's shipment

### Reward Function
```
Reward = 4 × (delivered) - (missed) - (purchased)
```

Value iteration computes the long-horizon strategy for maximizing expected profit.

## Contact

For issues or questions, please:
* Open a GitHub issue
* Email: 25chenghua@gmail.com