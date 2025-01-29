```markdown
# Cabbage Merchant MDP

A Markov Decision Process (MDP) approach to the “Cabbage Merchant Problem,” where we manage daily orders and uncertain shipments of cabbages with a 15% cancellation probability. This repository contains:

---

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
├── requirements.txt
```

1. **`results/`**  
   - `policy.npy` and `value_function.npy` store the converged optimal policy and value function, respectively.

2. **`src/`**  
   - `value_iteration.py` implements the MDP model and runs value iteration.  
   - `simulation.py` simulates business operations using the optimal policy.

---

## Installation

1. **Clone the Repo**
   ```bash
   git clone <repo-url> cabbage-merchant-mdp
   cd cabbage-merchant-mdp
   ```

2. **(Optional) Create and Activate a Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

---

## Running Value Iteration

In the `src/` directory:

```bash
python value_iteration.py
```
This runs a value iteration algorithm that may take up to an hour (depending on chosen parameters) to produce two files in `results/`:
- **`policy.npy`**  
- **`value_function.npy`**

---

## Running Simulation

After generating the policy, you can simulate day-by-day performance:

```bash
python simulation.py
```

The simulation will:
1. Load `policy.npy` from the `results/` folder.
2. Step through the MDP for a specified number of days.
3. Print total and average daily profit.

---

## MDP Model Overview

1. **State**:  
   \((O_1,O_2,O_3,\;A_1,A_2,\;c_1,c_2)\)  
   - \(O_i\): # of orders to fulfill in \(i\) days  
   - \(A_j\): # of cabbages arriving in \(j\) days  
   - \(c_j\in\{0,1\}\): cancellation flags for the corresponding shipments  

2. **Action**:  
   - **Accept** (1) or **reject** (0) the incoming daily order  
   - **Buy** 0–5 cabbages for delivery in 2 days  

3. **Transition**:
   - If \(c_1=0\), the day’s shipment arrives; else no arrivals.  
   - Deliver cabbages to meet \(O_1\).  
   - Shift \(O_1\leftarrow O_2\), \(O_2\leftarrow O_3\), etc.  
   - Draw a new cancellation flag for day‐after‐tomorrow’s shipment.

4. **Reward**:  
   \[
   4 \times (\text{delivered}) \;-\; (\text{missed}) \;-\; (\text{purchased}).
   \]

Value iteration computes the long-horizon strategy for maximizing expected profit.

---

## Contact

For issues or questions, please open a GitHub issue or reach out to 25chenghua@gmail.com.
```