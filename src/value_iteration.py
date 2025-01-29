import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

def value_iteration(
    max_O=5,   # max orders to track (O1,O2,O3)
    max_A=5,   # max cabbages to track (A1,A2)
    p_cancel=0.15,
    gamma=1.0,  
    theta=1e-6,
    max_iter=10000,
):
    """
    Value Iteration for the cabbage merchant MDP.
    
    Args:
        max_O (int): Maximum orders to track (O1,O2,O3)
        max_A (int): Maximum cabbages to track (A1,A2)
        p_cancel (float): Probability of cancellation
        gamma (float): Discount factor
        theta (float): Convergence threshold
        max_iter (int): Maximum iterations
        
    Returns:
        tuple: (value_function, policy)
    """
    # Initialize value function and policy using numpy arrays
    # Shape: (max_O+1, max_O+1, max_O+1, max_A+1, max_A+1, 2, 2)
    V = np.zeros((max_O+1, max_O+1, max_O+1, max_A+1, max_A+1, 2, 2))
    policy = np.zeros((max_O+1, max_O+1, max_O+1, max_A+1, max_A+1, 2, 2, 2), dtype=int)
    
    # All possible actions
    actions = [(accept, purchase) 
              for accept in [0, 1] 
              for purchase in range(6)]

    def next_state_and_reward(state_idx, action):
        """Calculate next states and rewards for a given state and action."""
        O1, O2, O3, A1, A2, c1, c2 = state_idx
        accept, purchase = action

        # Compute immediate reward
        arriving_cabbages = A1 if c1 == 0 else 0
        delivered = min(O1, arriving_cabbages)
        missed = O1 - delivered
        immediate_reward = 4 * delivered - missed - purchase

        # Compute next state components
        next_O1 = O2
        next_O2 = O3
        next_O3 = min(O3 + accept, max_O)
        next_A1 = A2
        next_A2 = min(purchase, max_A)
        next_c1 = c2

        # Return transitions for both possible values of next_c2
        transitions = []
        # Case 1: Not canceled (c2=0)
        s_ok = (next_O1, next_O2, next_O3, next_A1, next_A2, next_c1, 0)
        transitions.append((s_ok, 1-p_cancel, immediate_reward))
        # Case 2: Canceled (c2=1)
        s_cx = (next_O1, next_O2, next_O3, next_A1, next_A2, next_c1, 1)
        transitions.append((s_cx, p_cancel, immediate_reward))

        return transitions

    # Value Iteration main loop
    for iteration in tqdm(range(max_iter), desc="Value Iteration"):
        delta = 0.0
        # Use numpy's ndindex to iterate over all state indices
        for state_idx in np.ndindex(V.shape):
            old_value = V[state_idx]
            best_value = float('-inf')
            best_act = (0, 0)

            for action in actions:
                outcomes = next_state_and_reward(state_idx, action)
                q_sa = 0.0
                for (next_state_idx, prob, reward) in outcomes:
                    q_sa += prob * (reward + gamma * V[next_state_idx])

                if q_sa > best_value:
                    best_value = q_sa
                    best_act = action

            delta = max(delta, abs(best_value - old_value))
            V[state_idx] = best_value
            policy[state_idx] = best_act

        if delta < theta:
            print(f"Converged in {iteration} iterations.")
            break

    return V, policy

def plot_convergence(deltas):
    """Plot the convergence of value iteration."""
    plt.figure(figsize=(8, 5))
    plt.plot(deltas, label="Delta per iteration")
    plt.xlabel("Iteration")
    plt.ylabel("Max Value Update (Delta)")
    plt.title("Value Iteration Convergence")
    plt.grid(True)
    plt.legend()
    plt.show()

if __name__ == "__main__":
    # Run value iteration
    V, policy = value_iteration()
    
    # Save results
    np.save("../results/value_function.npy", V)
    np.save("../results/policy.npy", policy)
    
    # Print some example optimal actions
    sample_states = [
        (0,0,0,0,0,0,0),
        (1,0,0,1,0,0,0),
        (2,2,0,2,1,0,1)
    ]
    print("\nOptimal actions for sample states:")
    for s in sample_states:
        print(f"State {s}: best action = {tuple(policy[s])}, value = {V[s]:.2f}") 