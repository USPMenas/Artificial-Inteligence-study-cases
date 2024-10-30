import numpy as np

# Define the transition matrix P
P = np.array([
    [0,   0,   0,   0,   1],    # From state 0 to 4
    [1/6, 5/6, 0,   0,   0],    # From state 1
    [0,   2/6, 4/6, 0,   0],    # From state 2
    [0,   0,   3/6, 3/6, 0],    # From state 3
    [0,   0,   0,   4/6, 2/6]    # From state 4
])

# Method 1: Using the Power Method to find the stationary distribution
# Initial guess for the stationary distribution
pi = np.array([1/5, 1/5, 1/5, 1/5, 1/5])  # Initial uniform distribution

tolerance = 10^(-6)
max_interations = 1000

for k in range(max_interations):
    pi_next = P.T @ pi # Update distribution
    pi_next = pi_next/np.sum(pi_next)
    if np.linalg.norm(pi_next - pi, 1) < tolerance:  # Check for convergence
        break
    pi = pi_next  # Update current distribution

# Display the stationary distribution
print('Stationary Distribution using Power Method:')
print(pi)

# Calculate the average number of bottles of water
average_bottles = np.sum(np.arange(len(pi)) * pi)
quantity = np.array([0, 1, 2, 3, 4])
av2 = np.sum(pi*quantity)

print("Average number of bottles of water in the fridge:", average_bottles)
print("\n Or:", av2)

# Method 2: Directly solve the equation pi*P = pi
# Setting up the system for the stationary distribution
A = P.T - np.eye(5)  # P.T is the transpose of P
A = np.vstack([A, np.ones(5)])  # Add normalization condition
b = np.array([0, 0, 0, 0, 0, 1])  # Last element is for normalization

# Solve the linear system
stationary_distribution = np.linalg.lstsq(A, b, rcond=None)[0]  # Use least squares solution
print('Stationary Distribution using Linear System:')
print(stationary_distribution)