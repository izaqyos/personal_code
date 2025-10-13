import numpy as np

def gradient_descent(X, y, learning_rate=0.01, num_iterations=1000):
    """Performs gradient descent for simple linear regression."""
    m, b = 0, 0  
    n = len(X) 
    for _ in range(num_iterations):
        y_pred = m * X + b 
        mse = np.mean((y - y_pred) ** 2)  # Mean Squared Error
        dm = (-2/n) * sum(X * (y - y_pred))  # Gradient of MSE w.r.t. slope
        db = (-2/n) * sum(y - y_pred)        # Gradient of MSE w.r.t. intercept
        m -= learning_rate * dm  
        b -= learning_rate * db 
    return m, b

X = np.array([1, 2, 3, 4, 5])
y = np.array([3, 5, 7, 9, 11])

m, b = gradient_descent(X, y)

print(f"Best-fit line: y = {m:.2f}x + {b:.2f}")

new_x = 6 
prediction = m * new_x + b
print(f"Predicted value for x={new_x}: {prediction:.2f}")
