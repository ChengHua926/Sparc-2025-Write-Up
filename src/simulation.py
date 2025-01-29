import numpy as np
import random
import matplotlib.pyplot as plt

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
            tuple: (total_profit, daily_profits)
        """
        random.seed(seed)
        state = (0, 0, 0, 0, 0, 0, 0)  # Initial state
        daily_profits = []
        total_profit = 0.0

        for day in range(n_days):
            # Get current state components
            O1, O2, O3, A1, A2, c1, c2 = state
            
            # Get action from policy
            accept, purchase = self.policy[O1, O2, O3, A1, A2, c1, c2]
            
            # Calculate daily results
            arriving_cabbages = A1 if c1 == 0 else 0
            delivered = min(O1, arriving_cabbages)
            missed = O1 - delivered
            
            # Calculate profit
            day_profit = 4*delivered - missed - purchase
            total_profit += day_profit
            daily_profits.append(day_profit)
            
            # Update state
            state = (
                O2,                             # next O1
                O3,                             # next O2
                min(O3 + accept, self.max_O),   # next O3
                A2,                             # next A1
                min(purchase, self.max_A),      # next A2
                c2,                             # next c1
                random.random() < self.p_cancel # next c2
            )
            
        return total_profit, daily_profits

    def plot_profits(self, daily_profits):
        """Plot the daily profits over time."""
        plt.figure(figsize=(10, 6))
        plt.plot(daily_profits)
        plt.xlabel("Day")
        plt.ylabel("Profit")
        plt.title("Daily Profits Over Time")
        plt.grid(True)
        plt.show()
        
        # Also show moving average
        window = min(100, len(daily_profits))
        moving_avg = np.convolve(daily_profits, 
                                np.ones(window)/window, 
                                mode='valid')
        plt.figure(figsize=(10, 6))
        plt.plot(moving_avg)
        plt.xlabel("Day")
        plt.ylabel(f"{window}-Day Moving Average Profit")
        plt.title("Moving Average of Daily Profits")
        plt.grid(True)
        plt.show()

def run_simulations(n_days_list=[100, 1000, 5000, 10000]):
    """Run multiple simulations with different durations."""
    # Load pre-computed policy
    policy = np.load("../results/policy.npy")
    simulator = CabbageSimulator(policy)
    
    results = []
    for n in n_days_list:
        total, daily = simulator.simulate(n_days=n)
        avg_profit = total/n
        print(f"For n_days={n:5d}, total profit={total:8.2f}, "
              f"average profit/day={avg_profit:.3f}")
        results.append((n, total, daily))
    
    # Plot results for the longest simulation
    simulator.plot_profits(results[-1][2])
    
    return results

if __name__ == "__main__":
    run_simulations() 