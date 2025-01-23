import numpy as np

# Define the HMM parameters

# Hidden states: "sunny", "rainy"
states = ['sunny', 'rainy']

# Observations: "umbrella" (1), "no umbrella" (0)
observations = ['no umbrella', 'umbrella']

# Initial state distribution: [P(sunny), P(rainy)]
initial_prob = np.array([0.5, 0.5])

# Transition probabilities between states
#        sunny    rainy
trans_prob = np.array([[0.8, 0.2],  # P(sunny -> sunny), P(sunny -> rainy)
                       [0.4, 0.6]])  # P(rainy -> sunny), P(rainy -> rainy)

# Emission probabilities for observations
#        no umbrella, umbrella
emission_prob = np.array([[0.9, 0.1],  # P(umbrella | sunny), P(no umbrella | sunny)
                          [0.2, 0.8]])  # P(umbrella | rainy), P(no umbrella | rainy)

# Sequence of observations: 1 = "umbrella", 0 = "no umbrella"
observed_sequence = [1, 1, 0, 1, 0]  # Observations over time

# Step 1: Filtering Algorithm (Recursive)

def forward_algorithm(obs_seq, init_prob, trans_prob, emit_prob):
    # Initialize forward probability for the first observation
    T = len(obs_seq)
    num_states = len(init_prob)

    # Forward probability matrix
    forward_prob = np.zeros((T, num_states))

    # Initial belief based on the first observation
    forward_prob[0, :] = init_prob * emit_prob[:, obs_seq[0]]

    # Recursive forward step for each time step t
    for t in range(1, T):
        for s in range(num_states):
            # Update belief state: predict and correct
            forward_prob[t, s] = np.sum(forward_prob[t-1, :] * trans_prob[:, s]) * emit_prob[s, obs_seq[t]]

    # Normalize the forward probabilities (for filtering)
    forward_prob[t, :] /= np.sum(forward_prob[t, :])

    return forward_prob

# Step 2: Apply the filtering algorithm
result = forward_algorithm(observed_sequence, initial_prob, trans_prob, emission_prob)

# Output the filtered probabilities at each time step
print("Filtered probabilities at each time step:")
for t in range(len(observed_sequence)):
    print(f"Time {t + 1}: P(sunny) = {result[t, 0]:.4f}, P(rainy) = {result[t, 1]:.4f}")
