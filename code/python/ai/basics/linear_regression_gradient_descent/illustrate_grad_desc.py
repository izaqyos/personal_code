import numpy as np
import matplotlib.pyplot as plt

# Generate some sample data points
x = np.array([1, 2, 3, 4, 5])
y = np.array([2, 4, 5, 4, 5])

# Define the learning rate (controls how much we update weights each step)
learning_rate = 0.01

# Initialize weights (random starting point)
m = np.random.rand()  # Slope (coefficient of x)
b = np.random.rand()  # Intercept (y-axis offset)

# Function to calculate the predicted y values based on our current weights
def predict(x):
  return m * x + b

# Function to calculate the mean squared error (MSE) loss
def mse(y_true, y_predicted):
  return np.mean((y_true - y_predicted) ** 2)

# Training loop (multiple iterations for gradient descent)
iterations = 1000
losses = []  # Track loss history for visualization

for i in range(iterations):
  # Calculate predicted y values based on current weights
  y_predicted = predict(x)

  # Calculate the loss (MSE)
  loss = mse(y, y_predicted)
  losses.append(loss)

  # Calculate the gradients of the loss function with respect to m and b
  # These represent the direction and magnitude of change for weight updates
  dm = -2 * np.mean(x * (y - y_predicted))
  db = -2 * np.mean(y - y_predicted)

  # Update weights using the learning rate and gradients
  m -= learning_rate * dm
  b -= learning_rate * db

  # Print update information (optional for tracking progress)
  if i % 100 == 0:
    print(f"Iteration: {i}, Loss: {loss:.4f}")

# Print final weights
print(f"Final weights: m = {m:.4f}, b = {b:.4f}")

# Generate predicted y values using the final weights
y_predicted = predict(x)

# Plot the data points and the fitted line
plt.plot(x, y, 'o', label='Data Points')
plt.plot(x, y_predicted, label='Fitted Line')
plt.xlabel('X')
plt.ylabel('Y')
plt.legend()
plt.show()

# Plot the loss history (optional for visualization)
plt.plot(losses)
plt.xlabel('Iteration')
plt.ylabel('MSE Loss')
plt.show()
