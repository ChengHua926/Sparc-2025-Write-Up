import numpy as np
import random
from pathlib import Path

class CabbageSimulator:
    def __init__(self, policy, max_O=5, max_A=5, p_cancel=0.15):
        """
        Initialize the simulator with a policy.
        
        Args:
            policy (np.ndarray): Pre-computed policy array
            max_O (int): Maximum orders to track
            max_A (int): Maximum cabbages to track
            p_cancel (float): Probability of cancellation
        """
        self.policy = policy
        self.max_O = max_O
        self.max_A = max_A
        self.p_cancel = p_cancel

    def simulate(self, n_days=1000, seed=42):
        """
        Simulate the merchant's business for n_days.
        
        Args:
            n_days (int): Number of days to simulate
            seed (int): Random seed for reproducibility
            
        Returns:
            tuple: (total_profit, daily_profits, metrics_dict)
        """
        random.seed(seed)
        state = (0, 0, 0, 0, 0, 0, 0)  # Initial state
        daily_profits = []
        total_profit = 0.0
        
        metrics = {
            'deliveries': 0,
            'missed_orders': 0,
            'purchases': 0,
            'cancellations': 0
        }

        for _ in range(n_days):
            O1, O2, O3, A1, A2, c1, c2 = state
            c1, c2 = int(c1), int(c2)
            
            accept, purchase = self.policy[O1, O2, O3, A1, A2, c1, c2]
            
            arriving_cabbages = A1 if c1 == 0 else 0
            delivered = min(O1, arriving_cabbages)
            missed = O1 - delivered
            
            metrics['deliveries'] += delivered
            metrics['missed_orders'] += missed
            metrics['purchases'] += purchase
            metrics['cancellations'] += c1
            
            day_profit = 4*delivered - missed - purchase
            total_profit += day_profit
            daily_profits.append(day_profit)
            
            state = (
                O2,                             # next O1
                O3,                             # next O2
                min(O3 + accept, self.max_O),   # next O3
                A2,                             # next A1
                min(purchase, self.max_A),      # next A2
                c2,                             # next c1
                int(random.random() < self.p_cancel) # next c2
            )
            
        for key in metrics:
            metrics[key] /= n_days
            
        return total_profit, daily_profits, metrics

def run_simulations(n_days_list=[1000, 5000, 10000, 50000]):
    """
    Run multiple simulations with different durations.
    
    Args:
        n_days_list (list): List of simulation durations to test
        
    Returns:
        list: List of tuples containing (n_days, total_profit, daily_profits, metrics)
    """
    policy_path = Path('../results/policy.npy')
    if not policy_path.exists():
        raise FileNotFoundError("Policy file not found. Run value_iteration.py first.")
    
    policy = np.load(policy_path)
    simulator = CabbageSimulator(policy)
    
    results = []
    for n in n_days_list:
        total, daily, metrics = simulator.simulate(n_days=n)
        avg_profit = total/n
        
        print(f"\nSimulation Results ({n:,} days)")
        print("-" * 40)
        print(f"Total Profit: {total:,.2f}")
        print(f"Average Daily Profit: {avg_profit:.2f}")
        print("\nOperational Metrics (Daily Averages)")
        print("-" * 40)
        for key, value in metrics.items():
            print(f"{key.replace('_', ' ').title():20}: {value:.2f}")
        
        results.append((n, total, daily, metrics))
    
    return results

if __name__ == "__main__":
    run_simulations() 